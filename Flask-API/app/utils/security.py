# 标准库导入
# 导入网络请求库
import requests
# 用于类型提示
from typing import List
# 用于日期时间处理
from datetime import datetime, timedelta

# 第三方库导入
# 用于密码哈希和验证
import bcrypt
# 用于JWT令牌生成和验证
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    verify_jwt_in_request
)

# 本地应用/库导入
# 项目配置文件
from config import Config
# 统一异常处理模块
from app.common.exceptions import fail
# 用户模型
from app.models.system.user import SysUser

# JWT工具类
class SecurityUtils:

    # 创建访问令牌和刷新令牌
    @staticmethod
    def create_tokens(identity):
        expires = (datetime.now() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)).strftime("%Y/%m/%d %H:%M:%S")
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return {"accessToken": access_token,"refreshToken": refresh_token,"expires": expires}
    
    # 刷新令牌
    @staticmethod
    def refresh_token(refresh_token: str) -> dict:
        access_token = create_access_token(identity=get_jwt_identity())
        expires = (datetime.now() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)).strftime("%Y/%m/%d %H:%M:%S")
        return {"accessToken": access_token,"refreshToken": refresh_token,"expires": expires}
    
    # 获取当前用户信息
    @staticmethod
    def get_current_user():
        verify_jwt_in_request()
        username = get_jwt_identity()
        user = SysUser.get_by_username(username)
        if not user:
            raise fail(401,"用户不存在")
        # 将当前用户信息存储到Flask的g对象中
        from flask import g
        g.current_user = username
        return user

    # 获取当前用户账号
    @staticmethod
    def get_current_username():
        verify_jwt_in_request()
        username = get_jwt_identity()
        # 将当前用户信息存储到Flask的g对象中
        from flask import g
        g.current_user = username
        return username
    
    # 是否有指定角色
    @staticmethod
    def has_roles(role_codes: List[str]) -> bool:
        user = SecurityUtils.get_current_user()
        user_roles = set([role.code for role in user.roles if not role.deleted])
        return bool(user_roles.intersection(set(role_codes)))

    @staticmethod
    def hash_password(password):
        """密码哈希"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """密码验证"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def wx_login(code: str) -> dict:
        url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={Config.WX_APPID}&secret={Config.WX_SECRET}&code={code}&grant_type=authorization_code"
        res = requests.get(url).json()
        if "errcode" in res: return False,f"微信登陆失败: {res['errmsg']}"
        url = f"https://api.weixin.qq.com/sns/userinfo?access_token={res['access_token']}&openid={res['openid']}"
        res = requests.get(url).json()
        if "errcode" in res: return False,f"微信获取用户信息失败: {res['errmsg']}"
        data = {
            "username": res["openid"],
            "nickname": res["nickname"].encode('iso-8859-1').decode('utf-8'),
            "avatar": res["headimgurl"],
            "sex": res["sex"]
        }
        return True,data