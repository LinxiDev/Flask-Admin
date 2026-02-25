# 导入 Pydantic 的 BaseModel 和 Field 用于数据模型定义
from typing import Optional
from pydantic import BaseModel, Field


class Login(BaseModel):
    username: str = Field(..., description="用户名", example="admin")
    password: str = Field(..., description="密码", example="123456")


class RefreshToken(BaseModel):
    Authorization: str = Field(..., description="刷新令牌", example="your_refresh_token_here")

class WxLogin(BaseModel):
    code: Optional[str] = Field(None, description="微信登录code", example="your_code_here")
    state: str = Field(..., description="微信登录state", example="your_state_here")