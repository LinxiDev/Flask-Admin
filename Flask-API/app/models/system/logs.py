# 导入日志输出模块
from loguru import logger
# 导入日期时间模块
from datetime import datetime
# 导入公共工具模块
from app.utils.common import CommonUtils
# 导入数据库对象
from app.common.extension import db
# 导入基础模型类
from app.models.base import BaseModel


class SysLoginLog(BaseModel):
    __tablename__ = 'sys_login_log'
    
    username = db.Column(db.String(50), nullable=False, default='', comment='用户账号')
    ip = db.Column(db.String(128), nullable=False, default='', comment='登录IP地址')
    address = db.Column(db.String(255), nullable=False, default='', comment='登录地点')
    browser = db.Column(db.String(50), nullable=False, default='', comment='浏览器类型')
    system = db.Column(db.String(50), nullable=False, default='', comment='操作系统')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='登录状态（1成功 0失败）')
    behavior = db.Column(db.String(255), nullable=False, default='', comment='提示消息')
    login_time = db.Column(db.DateTime, default=datetime.now, comment='访问时间')

    # 记录账号密码登陆日志
    @staticmethod
    def create(username: str, ip, ua, status = 0, behavior="账号登陆") -> None:
        address, system, browser = CommonUtils.get_request_info(ip, ua)
        # 保存到数据库
        log = SysLoginLog(
            username=username, 
            ip=ip, 
            address=address, 
            browser=browser, 
            system=system, 
            status=status, 
            behavior=behavior,
            login_time=datetime.now()
        )
        log.save()
        if status == 1:
            logger.success(f"登陆成功: {username} IP: {ip} 设备:{system} {browser} 渠道: {behavior}")
        else:
            logger.error(f"登陆失败: {username} IP: {ip} 设备:{system} {browser} 渠道: {behavior}")


class SysOperLog(BaseModel):
    __tablename__ = 'sys_operation_log'
    
    username = db.Column(db.String(50), nullable=False, index=True, comment='用户名')
    ip = db.Column(db.String(45), nullable=True, comment='操作者IP地址')
    address = db.Column(db.String(255), nullable=True, comment='地理位置')
    system = db.Column(db.String(50), nullable=True, comment='操作系统')
    browser = db.Column(db.String(50), nullable=True, comment='浏览器')
    status = db.Column(db.SmallInteger, nullable=False, comment='操作状态 (1 成功, 0 失败)')
    summary = db.Column(db.Text, nullable=True, comment='操作概要')
    module = db.Column(db.String(100), nullable=True, comment='所属模块')
    operating_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='操作时间')

    # 记录操作日志
    @staticmethod
    def create(module: str, summary: str, status: int, ip: str, username: str, address: str, system: str, browser: str):
        # 添加到数据库
        log = SysOperLog(
            username=username, 
            ip=ip, 
            address=address, 
            system=system, 
            browser=browser, 
            status=status, 
            summary=summary, 
            module=module,
            operating_time=datetime.now()
        )
        log.save()
        if status == 1:
            logger.success(f"操作成功: {username} IP: {ip} 设备:{system} {browser} 模块: {module} 概要: {summary}")
        else:
            logger.error(f"操作失败: {username} IP: {ip} 设备:{system} {browser} 模块: {module} 概要: {summary}")


class SystemLogs(BaseModel):
    __tablename__ = 'sys_system_log'

    level = db.Column(db.Integer, nullable=False, default=1, comment='日志级别 (0 debug, 1 info, 2 warn, 3 error, 4 fatal)')
    module = db.Column(db.String(100), nullable=False, default='', index=True, comment='所属模块')
    url = db.Column(db.String(500), nullable=False, index=True, comment='请求接口URL')
    method = db.Column(db.String(10), nullable=False, comment='请求方法 (GET, POST, PUT, DELETE 等)')
    ip = db.Column(db.String(45), nullable=True, comment='客户端IP地址')
    address = db.Column(db.String(255), nullable=True, comment='地理位置')
    system = db.Column(db.String(50), nullable=True, comment='操作系统')
    browser = db.Column(db.String(50), nullable=True, comment='浏览器')
    takes_time = db.Column(db.Integer, nullable=True, comment='请求耗时 (单位: 毫秒 ms)')
    request_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True, comment='请求时间')
    # 使用 JSON 类型存储 headers，需要数据库支持
    response_headers = db.Column(db.JSON, nullable=True, comment='响应头 (JSON格式)')
    # 使用 LONGTEXT 存储 body，避免 JSON 类型对大型对象的限制
    response_body = db.Column(db.JSON, nullable=True, comment='响应体')
    request_headers = db.Column(db.JSON, nullable=True, comment='请求头 (JSON格式)')
    request_body = db.Column(db.JSON, nullable=True, comment='请求体')
    trace_id = db.Column(db.String(64), nullable=True, index=True, comment='链路追踪ID')

    # 记录系统日志
    @staticmethod
    def create(module: str, request_time: datetime, request_headers: dict, request_body: str, response_headers: dict, response_body: str, takes_time: int, trace_id: str, level: int, url: str, method: str, ip: str, address: str, system: str, browser: str):
        # 添加到数据库
        log = SystemLogs(
            module=module, 
            url=url, 
            method=method, 
            ip=ip, 
            address=address, 
            system=system, 
            browser=browser, 
            takes_time=takes_time, 
            request_time=request_time, 
            response_headers=response_headers, 
            response_body=response_body, 
            request_headers=request_headers, 
            request_body=request_body, 
            trace_id=trace_id, 
            level=level
        )
        log.save()
