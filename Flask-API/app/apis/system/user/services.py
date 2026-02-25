# 导入os模块
import os
# 导入时间模块
import time
# 导入uuid模块
import uuid
# 导入base64模块
import base64
# 导入日志模块
from loguru import logger 
# 导入类型定义
from typing import Union
# 导入查询条件or
from sqlalchemy import or_
# 导入数据库操作对象
from app.common.extension import db
# 导入权限工具类
from app.utils import SecurityUtils
# 导入统一响应
from app.common.exceptions import APIException
# 导入用户模型
from app.models import SysUser,SysDept,SysUserDept,SysUserRole
# 导入数据模型定义
from .schemas import Query, Create, Update,RoleIds,ResetPassword,AssignRole,Avatar


class Services:
    @staticmethod
    def list(q:Query) -> list:
        if q.deptId is not None:
            query = query = SysUser.query.join(SysUserDept, SysUser.id == SysUserDept.user_id).join(SysDept, SysUserDept.dept_id == SysDept.id).filter(SysUser.deleted == 0).filter(SysDept.deleted == 0,SysDept.id == q.deptId)
        else:
            query = SysUser.query.filter_by(deleted=0)
        # name 同时查询用户名称和用户昵称
        query = query.filter(or_(SysUser.username.ilike(f"%{q.username}%"),SysUser.nickname.ilike(f"%{q.username}%"))) if q.username is not None and q.username.strip() else query
        query = query.filter(SysUser.status == q.status) if q.status is not None else query
        query = query.filter(SysUser.phone.ilike(f"%{q.phone}%")) if q.phone is not None else query
        query = query.order_by(SysUser.create_time).all()
        return [{**user.to_dict(),'dept':{'id':user.dept[0].id,'name':user.dept[0].dept_name}} for user in query]
    
    @staticmethod
    def add(body: Create) -> dict:
        user = SysUser.query.filter_by(username=body.username).first()
        if user is not None:
            raise APIException(msg="用户已存在")
        user = SysUser(
            username=body.username,
            nickname=body.nickname,
            phone=body.phone,
            email=body.email,
            sex=body.sex,
            status=body.status,
            remark=body.remark
        )
        user.password = SecurityUtils.hash_password(body.password)
        # 使用基础模型的save方法
        user.save()
        # 添加用户和部门关联
        user_dept = SysUserDept(user_id=user.id, dept_id=body.deptId)
        db.session.add(user_dept)
        db.session.commit()
        return None
    
    @staticmethod
    def delete(ids: Union[int, str]) -> dict:
        ids = [int(id) for id in ids.split(',')]
        # 使用基础模型的get_by_ids方法
        users = SysUser.get_by_ids(ids)
        for user in users:
            # 使用基础模型的update方法
            user.update(deleted=1)
        # 删除用户部门关联
        SysUserDept.query.filter(SysUserDept.user_id.in_(ids)).delete()
        # 删除用户角色关联
        SysUserRole.query.filter(SysUserRole.user_id.in_(ids)).delete()
        db.session.commit()
        return None
    
    @staticmethod
    def edit(body: Update) -> dict:
        # 使用基础模型的get_by_id方法
        user = SysUser.get_by_id(body.id)
        if user is None:
            raise APIException(msg="用户不存在")
        update_data = {}
        if body.nickname: update_data['nickname'] = body.nickname
        if body.phone: update_data['phone'] = body.phone
        if body.email: update_data['email'] = body.email
        if body.sex is not None: update_data['sex'] = body.sex
        if body.status is not None: update_data['status'] = body.status
        if body.remark: update_data['remark'] = body.remark
        # 使用基础模型的update方法
        user.update(**update_data)
        # 查询用户部门关联
        user_dept = SysUserDept.query.filter_by(user_id=body.id).first()
        # 是否与修改部门一致
        if user_dept.dept_id != body.deptId and body.deptId:
            user_dept.dept_id = body.deptId
            db.session.add(user_dept)
            db.session.commit()
        return None
    
    @staticmethod
    def change_password(body: ResetPassword) -> dict:
        # 使用基础模型的get_by_id方法
        user = SysUser.get_by_id(body.id)
        if user is None or user.deleted != 0:
            raise APIException(msg="用户不存在")
        # 使用基础模型的update方法
        user.update(password=SecurityUtils.hash_password(body.password))
        return None
    
    @staticmethod
    def upload_avatar(body: Avatar) -> dict:
        # 移除 data:image/png;base64,
        body.avatar = body.avatar.split(',')[1]
        # 将Base64编码的图片数据转换为bytes
        avatar_data = base64.b64decode(body.avatar)
        # 保存图片到upload/avatar目录下,命名为时间戳yyyyMMddHHmmss-uuid.png
        avatar_path = f"{int(time.time() * 1000)}-{uuid.uuid4()}.png"
        os.makedirs("upload/avatar", exist_ok=True)
        with open(f"upload/avatar/{avatar_path}", "wb") as f:
            f.write(avatar_data)
        logger.info(f"成功解码用户 {body.id} 的头像数据，大小: {len(avatar_data)} 字节")
        # 使用基础模型的get_by_id方法
        user = SysUser.get_by_id(body.id)
        # 判断用户是否存在
        if user is None or user.deleted != 0:
            raise APIException(msg="用户不存在")
        # 判断用户是否已存在头像,并且文件存在
        if user.avatar is not None and user.avatar != "":
            # 先删除旧头像
            old_avatar_path = user.avatar.split("/")[-1]
            if os.path.exists(f"upload/avatar/{old_avatar_path}"):
                os.remove(f"upload/avatar/{old_avatar_path}")
        # 使用基础模型的update方法
        user.update(avatar="/api/comm/upload/avatar/" + avatar_path)
        return None
    
    @staticmethod
    def get_roleIds(userId:Union[int,str]) -> list:
        # 使用基础模型的get_by_id方法
        user = SysUser.get_by_id(userId)
        if user is None or user.deleted != 0:
            return []
        return [role.id for role in user.roles if not role.deleted]


    @staticmethod
    def assign_role(body: AssignRole) -> dict:
        # 使用基础模型的get_by_id方法
        user = SysUser.get_by_id(body.id)
        if user is None or user.deleted != 0:
            raise APIException(msg="用户不存在")
        # 删除用户角色关联
        SysUserRole.query.filter_by(user_id=body.id).delete()
        # 添加用户角色关联
        for roleId in body.roleIds:
            user_role = SysUserRole(user_id=body.id, role_id=roleId)
            db.session.add(user_role)
        db.session.commit()
        return None


