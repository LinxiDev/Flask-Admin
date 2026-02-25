# 标准库导入
# 用于获取异常堆栈信息
import traceback

# 第三方库导入
# 日志记录模块
from loguru import logger
# Flask请求对象
from flask import request
# Pydantic数据格式校验异常
from pydantic import ValidationError
# HTTP异常模块
from werkzeug.exceptions import HTTPException
# Flask-JWT-Extended异常模块
from flask_jwt_extended.exceptions import JWTExtendedException

# 本地应用/库导入
# JWT扩展模块
from .extension import jwt
# 统一响应模块
from app.common.responses import fail

# 业务异常类
class APIException(Exception):
    def __init__(self, msg="操作失败", code=400):
        self.msg = msg
        self.code = code
        super().__init__(self.msg)

# 注册全局异常处理器
def register_exception_handlers(app):

    # 处理数据格式校验异常
    @app.errorhandler(ValidationError)
    def handle_validation_exception(e):
        logger.error(f"Pydantic验证异常 - 请求路径: {request.path}, 请求方法: {request.method}, 错误详情: {str(e)}")
        return fail(400, "请求参数验证失败")
    
    # 处理JWT校验异常
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_exception(e):
        logger.error(f"JWT异常 - 错误详情: {str(e)}")
        return fail(401, "认证失败,请重新登录")
    
    # 处理HTTP异常
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        logger.error(f"HTTP异常 - 错误详情: {str(e)}")
        http_msg_map = {
            400: "请求参数错误",
            401: "未授权访问",
            403: "禁止访问",
            404: "资源不存在",
            405: "请求方式错误",
            406: "请求格式不支持",
            408: "请求超时",
            409: "请求冲突",
            410: "资源已删除",
            411: "需要Content-Length头",
            412: "请求条件不满足",
            413: "请求实体过大",
            414: "请求URL过长",
            415: "不支持的媒体类型",
            416: "请求范围不符合要求",
            417: "预期结果不满足",
            418: "我是一个茶壶",
            421: "请求被重定向到多个位置",
            422: "请求实体无法处理",
            423: "资源被锁定",
            424: "依赖失败",
            425: "请求过早",
            426: "需要升级协议",
            428: "需要前置条件",
            429: "请求过于频繁",
            431: "请求头字段过大",
            451: "法律原因禁止访问",
            500: "服务器内部错误",
            501: "请求方法未实现",
            502: "网关错误",
            503: "服务不可用",
            504: "网关超时",
            505: "HTTP版本不支持",
            506: "变体也协商",
            507: "存储不足",
            508: "检测到无限循环",
            510: "需要扩展",
            511: "需要网络身份验证"
        }

        msg = http_msg_map.get(e.code, e.description)
        return fail(e.code, msg)

    # 处理通用异常
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"全局通用异常 - 错误详情: {str(e)}\n{traceback.format_exc()}")
        exception_msg_map = {
            "TypeError": "类型错误",
            "ValueError": "值错误",
            "NameError": "名称错误",
            "AttributeError": "属性错误",
            "KeyError": "键错误",
            "IndexError": "索引错误",
            "ZeroDivisionError": "除零错误",
            "OverflowError": "溢出错误",
            "FloatingPointError": "浮点错误",
            "AssertionError": "断言错误",
            "ImportError": "导入错误",
            "ModuleNotFoundError": "模块未找到",
            "SyntaxError": "语法错误",
            "IndentationError": "缩进错误",
            "IOError": "IO错误",
            "FileNotFoundError": "文件未找到",
            "PermissionError": "权限错误",
            "IntegrityError": "数据完整性错误",
            "ProgrammingError": "SQL编程错误",
            "OperationalError": "数据库操作错误",
            "DatabaseError": "数据库错误",
            "InterfaceError": "数据库接口错误",
            "TimeoutError": "超时错误",
            "ConnectionError": "连接错误",
            "OSError": "操作系统错误",
            "RuntimeError": "运行时错误",
            "NotImplementedError": "未实现错误",
            "KeyboardInterrupt": "键盘中断",
            "SystemExit": "系统退出"
        }

        exception_type = type(e).__name__
        msg = exception_msg_map.get(exception_type, "服务器内部错误")
        return fail(msg=msg, code=500)
    
    # 接口返回异常
    @app.errorhandler(APIException)
    def handle_api_exception(e):
        logger.error(f"返回异常失败: {str(e)}")
        return fail(msg=e.msg, code=e.code)
    

# 当请求缺少 JWT Token 时的回调
@jwt.unauthorized_loader
def handle_unauthorized_error(err_str):
    logger.error(f"JWT未授权异常 - 错误详情: {err_str}")
    return fail(401, "请先登陆")

# 当 JWT Token 无效时的回调
@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    logger.error(f"JWT令牌过期异常 - 令牌头: {jwt_header}, 令牌载荷: {jwt_payload}")
    return fail(401, "登录已过期,请重新登录")

# 当JWT Token 为非法时的回调
@jwt.invalid_token_loader
def handle_invalid_token(err_str):
    logger.error(f"JWT令牌无效异常 - 错误详情: {err_str}")
    return fail(401, "登录凭证无效，请重新登录")

