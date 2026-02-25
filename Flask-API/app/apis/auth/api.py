# 导入Flask 蓝本模块
from flask import Blueprint,request
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入统一返回响应模块
from app.common.responses import success,fail
# 导入jwt_extended 模块
from flask_jwt_extended import jwt_required
# 导入数据模型定义
from .schemas import Login,RefreshToken,WxLogin

# 创建认证蓝图
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
@siwa.doc(body=Login,tags=["认证"], summary="用户登录")
def login(body: Login):
    return success(Services.login(body.username, body.password))

@bp.route('/refreshToken', methods=['GET'])
@siwa.doc(header=RefreshToken,tags=["认证"], summary="刷新Token")
@jwt_required(refresh=True)
def refresh_token():
    refreshToken = request.headers.get("Authorization")
    return success(Services.refresh_token(refreshToken))

@bp.route('/getRouters', methods=['GET'])
@siwa.doc(tags=["认证"], summary="获取用户路由权限")
@jwt_required()
def get_routers():
    return success(Services.get_routers())


@bp.route('/wxLogin', methods=['GET'])
@siwa.doc(query=WxLogin,tags=["认证"], summary="微信登录")
def wx_login(query: WxLogin):
    resp = Services.wx_login(query.code,query.state)
    if resp is None:
        return fail(200,"等待微信扫码授权...")
    elif "html" in resp:
        return resp
    else:
        return success(resp)