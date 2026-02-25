# 导入类型定义
from typing import Union
# 导入用户模型
from app.models import SysDept
# 导入数据库操作对象
from app.common.extension import db
# 导入统一响应
from app.common.exceptions import APIException
# 导入数据模型
from .schemas import Query,Create,Update

class Services:
    @staticmethod
    def list(q: Query) -> list:
        # 构建查询条件
        conditions = {"deleted": 0}
        if q.name is not None and q.name.strip():
            query = SysDept.query.filter_by(**conditions).filter(SysDept.dept_name.ilike(f"%{q.name}%"))
        else:
            query = SysDept.query.filter_by(**conditions)
        
        if q.status is not None:
            query = query.filter(SysDept.status == q.status)
            
        query = query.order_by(SysDept.order_num.asc())
        depts = query.all()
        
        return [
            {
                "id": dept.id,
                "name": dept.dept_name,
                "parentId": dept.parent_id,
                "phone": dept.phone,
                "principal": dept.leader,
                "remark": dept.remark,
                "sort": dept.order_num,
                "status": dept.status,
                "email": dept.email,
                "createTime": dept.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            for dept in depts
        ]
    
    @staticmethod
    def add(body: Create) -> None:
        # 将数据模型转为数据库对象
        dept = SysDept(
            parent_id=body.parentId,
            dept_name=body.name,
            order_num=body.sort,
            leader=body.leader,
            phone=body.phone,
            email=body.email,
            status=body.status,
            remark=body.remark
        )
        # 使用基础模型的save方法
        dept.save()
        return None
    
    @staticmethod
    def delete(ids: Union[int, str]) -> None:
        id_list = [int(id_) for id_ in str(ids).split(",") if id_.isdigit()]
        # 使用批量更新，保留原逻辑
        SysDept.query.filter(SysDept.id.in_(id_list)).update({"deleted": 1}, synchronize_session=False)
        db.session.commit() 
        return None
    
    @staticmethod
    def edit(body: Update) -> None:
        # 使用基础模型的get_by_id方法
        dept = SysDept.get_by_id(body.id)
        if not dept or dept.deleted != 0:
            raise APIException("该部门不存在")
        
        # 使用基础模型的update方法
        dept.update(
            dept_name=body.name,
            parent_id=body.parentId,
            order_num=body.sort,
            leader=body.leader,
            phone=body.phone,
            email=body.email,
            status=body.status,
            remark=body.remark
        )
        return None