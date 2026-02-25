# 导入类型定义
from typing import Union
# 导入数据库操作对象
from app.common.extension import db
# 导入统一响应
from app.common.exceptions import APIException
# 导入用户模型
from app.models import SysRole,SysMenu,SysUserRole,SysRoleMenu
# 导入数据模型定义
from .schemas import Query,Create,Update,assignMenu


class Services:
    @staticmethod
    def list(q: Query) -> list:
        query = SysRole.query.filter_by(deleted=0)
        query = query.filter(SysRole.name.ilike(f"%{q.name}%")) if q.name is not None and q.name.strip() else query
        query = query.filter(SysRole.code.ilike(f"%{q.code}%")) if q.code is not None and q.code.strip() else query
        query = query.filter(SysRole.status == q.status) if q.status is not None else query
        query = query.order_by(SysRole.create_time).all()
        return [{
            "id":role.id,
            "name":role.name,
            "code":role.code,
            "status":role.status,
            "remark":role.remark,
            "createTime":role.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "updateTime":role.update_time.strftime("%Y-%m-%d %H:%M:%S") if role.update_time else None,
        } for role in query]
    
    @staticmethod
    def listAll() -> list:
        query = SysRole.query.filter_by(deleted=0)
        query = query.order_by(SysRole.create_time).all()
        return [{
            "id":role.id,
            "name":role.name
        } for role in query]
    
    @staticmethod
    def add(body: Create) -> dict:
        role = SysRole.query.filter_by(name=body.name).first()
        if role:
            raise APIException(msg="角色名称已存在")
        role = SysRole.query.filter_by(code=body.code).first()
        if role:
            raise APIException(msg="角色编码已存在")
        role = SysRole(name=body.name,code=body.code,status=1,remark=body.remark)
        # 使用基础模型的save方法
        role.save()
        return None
    
    @staticmethod
    def delete(ids: Union[int,str]) -> dict:
        ids = [int(id) for id in ids.split(',')]
        # 使用基础模型的get_by_ids方法
        roles = SysRole.get_by_ids(ids)
        for role in roles:
            # 使用基础模型的update方法
            role.update(deleted=1)
        # 删除角色用户关联
        SysUserRole.query.filter(SysUserRole.role_id.in_(ids)).delete()
        # 删除角色菜单关联
        SysRoleMenu.query.filter(SysRoleMenu.role_id.in_(ids)).delete()
        db.session.commit()
        return None
    
    @staticmethod
    def edit(body: Update):
        # 使用基础模型的get_by_id方法
        role = SysRole.get_by_id(body.id)
        if not role:
            raise APIException(msg="角色不存在")
        update_data = {}
        if body.name: update_data['name'] = body.name
        if body.code: 
            if SysRole.query.filter_by(code=body.code).first() and role.code != body.code:
                raise APIException(msg="角色编码已存在")
            update_data['code'] = body.code
        if body.status is not None: update_data['status'] = body.status
        if body.remark: update_data['remark'] = body.remark
        # 使用基础模型的update方法
        role.update(**update_data)
        return None
    
    @staticmethod
    def getRoleMenu():
        query = SysMenu.query.with_entities(SysMenu.parent_id,SysMenu.id,SysMenu.type,SysMenu.title).order_by(SysMenu.rank).all()
        return [{
            "parentId":menu.parent_id,
            "id":menu.id,
            "menuType":menu.type,
            "title":menu.title
        } for menu in query]
    
    @staticmethod
    def getRoleMenuIds(roleId: int):
        # 使用基础模型的get_by_id方法
        role = SysRole.get_by_id(roleId)
        if not role or role.deleted != 0:
            raise APIException(msg="角色不存在")
        if role.code == "admin":
            # 使用基础模型的get_all方法
            return [menu.id for menu in SysMenu.get_all()]
        query = SysRoleMenu.query.filter_by(role_id=roleId).all()
        return [menu.menu_id for menu in query]

    @staticmethod
    def assignMenu(body: assignMenu):
        # 使用基础模型的get_by_id方法
        role = SysRole.get_by_id(body.id)
        if not role or role.deleted != 0:
            raise APIException(msg="角色不存在")
        SysRoleMenu.query.filter_by(role_id=body.id).delete()
        for menuId in body.menuIds:
            db.session.add(SysRoleMenu(role_id=body.id,menu_id=menuId))
        db.session.commit()
        return None