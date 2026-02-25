# 标准库导入
# 用于生成唯一标识符
import uuid
# 用于装饰器实现
from functools import wraps
# 用于日期时间处理
from datetime import datetime
# 用于异步日志记录
from concurrent.futures import ThreadPoolExecutor

# 第三方库导入
# Flask请求对象
from flask import request
# 导入jwt_extended 模块
from flask_jwt_extended import jwt_required

# 本地应用/库导入
# Flask应用实例
from app.core import app
# 导入统一返回响应模块
from app.common.responses import fail
# 公共工具模块
from app.utils.common import CommonUtils
# 安全工具模块
from app.utils.security import SecurityUtils
# 日志模型和记录器
from app.models.system.logs import SysOperLog, SystemLogs, logger

# 创建线程池用于异步日志记录
log_executor = ThreadPoolExecutor(max_workers=10)

# 权限检查装饰器: 检查用户是否具有指定权限 如 @hasPermi("sys:dept:list")
def hasPermi(auth: str):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            # 获取当前用户信息
            user = SecurityUtils.get_current_user()
            
            # 检查用户是否为admin角色
            user_roles = [role.code for role in user.roles if not role.deleted]
            if "admin" in user_roles:
                # admin用户默认拥有所有权限
                return f(*args, **kwargs)
            
            # 获取用户所有权限
            user_permissions = []
            for role in user.roles:
                if not role.deleted:
                    for menu in role.menus:
                        if menu.auths and menu.auths not in user_permissions:
                            user_permissions.append(menu.auths)
            
            # 检查是否具有指定权限
            if auth not in user_permissions:
                return fail(403, "无权限访问")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 日志装饰器(记录操作日志、系统日志)-异步记录避免影响请求性能
def record_log(module: str, summary: str = None, level: int = 1) -> None:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成追踪ID
            trace_id = str(uuid.uuid4()).replace('-', '')
            # 记录开始时间
            start_time = datetime.now()
            # 记录请求Path和方法
            req_path = request.path
            req_method = request.method
            # 记录IP
            ip = request.headers.get('X-Real-IP') or request.remote_addr
            # 获取UA信息
            ua = request.headers.get('User-Agent','')
            # 获取请求头数据
            req_headers = dict(request.headers or {})
            # 获取请求体数据
            try:
                req_body = dict(request.args or {}) or dict(request.form or {}) or dict(request.json or {})
            except Exception:
                req_body = {}
            # 获取用户名
            try:
                username = SecurityUtils.get_current_username()
            except Exception:
                username = ''
            try:
                # # 执行原函数
                result = func(*args, **kwargs)
                # 计算耗时（转换为毫秒）
                end_time = datetime.now()
                takes_time_ms = int((end_time - start_time).total_seconds() * 1000)
                # 处理响应数据
                if isinstance(result, tuple):
                    temp_result = result[0]
                else:
                    temp_result = result
                # 获取响应头数据
                if hasattr(temp_result, 'headers'):
                    resp_headers = dict(temp_result.headers or {})
                else:
                    resp_headers = {}
                # 处理响应体数据
                if hasattr(temp_result,'direct_passthrough'):
                    resp_body = dict(temp_result.json or {}) or dict(temp_result.data or {})
                else:
                    resp_body = {"msg": "特殊响应数据格式,不记录相关响应数据"}
                # 异步记录日志
                # SystemLogs.save(module,request_time, req_headers, req_body, resp_headers, resp_body, takes_time_ms, trace_id, level)
                log_executor.submit(_async_log_save,module,summary,1,start_time,req_headers,req_body,resp_headers,resp_body,takes_time_ms,trace_id,level,ip,ua,username,req_path,req_method)
                #_async_log_save(module,summary,1,start_time,req_headers,req_body,resp_headers,resp_body,takes_time_ms,trace_id,level,ip,ua,username,req_path,req_method)
                return result
            except Exception as e:
                # 发生异常时也记录日志
                end_time = datetime.now()
                takes_time_ms = int((end_time - start_time).total_seconds() * 1000)
                resp_body = str(e)
                log_executor.submit(_async_log_save,module,summary,0,start_time,req_headers,req_body,{},resp_body,takes_time_ms,trace_id,level,ip,ua,username,req_path,req_method)
                #_async_log_save(module,summary,0,start_time,req_headers,req_body,{},resp_body,takes_time_ms,trace_id,level,ip,ua,username,req_path,req_method)
                raise e
        return wrapper
    return decorator

def _async_log_save(module, summary, status, request_time, request_headers, request_body, response_headers, response_body, takes_time, trace_id, level, ip, ua, username, req_path, req_method):
    try:
        with app.app_context():
            # 获取请求信息
            address, system, browser = CommonUtils.get_request_info(ip,ua)
            # 保存操作日志
            if summary and username:
                SysOperLog.create(module, summary, status, ip, username, address, system, browser)
            # 保存系统日志
            SystemLogs.create(module=module,request_time=request_time,request_headers=request_headers,request_body=request_body,response_headers=response_headers,response_body=response_body,takes_time=takes_time,trace_id=trace_id,level=level,url=req_path,method=req_method,ip=ip,address=address,system=system,browser=browser)
            # 记录成功日志
            if status == 1:
                logger.success(f"日志记录成功 TraceId: {trace_id} URL: {req_path} 方法: {req_method} 耗时: {takes_time}ms")
            else:
                logger.error(f"日志记录异常 TraceId: {trace_id} URL: {req_path} 方法: {req_method} 耗时: {takes_time}ms")
    except Exception as log_error:
            # 如果日志记录本身出错，记录错误但不影响主流程
            logger.error(f"日志保存失败: {log_error}")