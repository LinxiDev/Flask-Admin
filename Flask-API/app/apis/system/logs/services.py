# 导入类型定义
from typing import Union
# 导入排序方法
from sqlalchemy import desc
# 导入数据库操作对象
from app.common.extension import db
# 导入统一响应
from app.common.exceptions import APIException
# 导入用户模型
from app.models import SysLoginLog,SysOperLog,SystemLogs
# 导入数据模型定义
from .schemas import LoginQuery,OperQuery,SysQuery

class Services:
    @staticmethod
    def login_list(body: LoginQuery) -> Union[dict, list]:
        query = SysLoginLog.query.order_by(desc(SysLoginLog.login_time))
        if body.username: query = query.filter(SysLoginLog.username.ilike(f"%{body.username}%"))
        if body.status is not None: query = query.filter(SysLoginLog.status == body.status)
        if body.loginTime and len(body.loginTime) == 2: query = query.filter(SysLoginLog.login_time.between(body.loginTime[0],body.loginTime[1]))
        query = query.limit(body.pageSize).offset((body.currentPage-1)*body.pageSize).all()
        return [log.to_dict() for log in query],body.currentPage,body.pageSize
            
    @staticmethod
    def delete_login_logs(ids: Union[int,str]):
        ids = [int(id) for id in ids.split(',')]
        # 使用基础模型的delete_by_ids方法
        SysLoginLog.delete_by_ids(ids)
        db.session.commit()
        return None
    
    @staticmethod
    def clear_login_logs():
        db.session.query(SysLoginLog).delete()
        db.session.commit()
        return None


    @staticmethod
    def operate_list(body: OperQuery) -> Union[dict, list]:
        query = SysOperLog.query.order_by(desc(SysOperLog.operating_time))
        if body.module: query = query.filter(SysOperLog.module.ilike(f"%{body.module}%"))
        if body.status is not None: query = query.filter(SysOperLog.status == body.status)
        if body.operatingTime and len(body.operatingTime) == 2: query = query.filter(SysOperLog.operating_time.between(body.operatingTime[0],body.operatingTime[1]))
        query = query.limit(body.pageSize).offset((body.currentPage-1)*body.pageSize).all()
        return [log.to_dict() for log in query],body.currentPage,body.pageSize
    
    @staticmethod
    def delete_operate_logs(ids: Union[int,str]):
        ids = [int(id) for id in ids.split(',')]
        # 使用基础模型的delete_by_ids方法
        SysOperLog.delete_by_ids(ids)
        db.session.commit()
        return None
    
    @staticmethod
    def clear_operate_logs():
        db.session.query(SysOperLog).delete()
        db.session.commit()
        return None


    @staticmethod
    def system_list(body: SysQuery)-> Union[dict, list]:
        query = SystemLogs.query.order_by(desc(SystemLogs.request_time))
        if body.module: query = query.filter(SystemLogs.module.ilike(f"%{body.module}%"))
        if body.requestTime and len(body.requestTime) == 2: query = query.filter(SystemLogs.request_time.between(body.requestTime[0],body.requestTime[1]))
        query = query.limit(body.pageSize).offset((body.currentPage-1)*body.pageSize).all()
        return [log.to_dict() for log in query],body.currentPage,body.pageSize
        

    @staticmethod
    def delete_system_logs(ids: Union[int,str]):
        ids = [int(id) for id in ids.split(',')]
        # 使用基础模型的delete_by_ids方法
        SystemLogs.delete_by_ids(ids)
        db.session.commit()
        return None
    
    @staticmethod
    def clear_system_logs():
        db.session.query(SystemLogs).delete()
        db.session.commit()
        return None
    
    @staticmethod
    def system_detail(id: Union[int,str]):
        # 使用基础模型的get_by_id方法
        log = SystemLogs.get_by_id(id)
        if log: return log.to_dict()
        raise APIException("系统日志不存在")
