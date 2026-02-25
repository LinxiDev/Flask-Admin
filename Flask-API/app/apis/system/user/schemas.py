# 导入 typing 的 Optional 和 List 用于类型提示
from typing import Optional, List
# 导入 Pydantic 的 BaseModel 和 Field 用于数据模型定义
from pydantic import BaseModel, Field, field_validator


class Query(BaseModel):
    deptId: Optional[int] = Field(None, description="部门ID", example=0)
    username: Optional[str] = Field(None, description="用户名称/用户昵称", example="小林")
    phone: Optional[str] = Field(None, description="手机号码", example="13800138000")
    status: Optional[int] = Field(None, description="用户状态（0正常 1停用）", example=0)

    # 将空字符串转换为None
    @field_validator('username', 'status','phone','deptId',mode='before')
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v
    

class Create(BaseModel):
    username: str = Field(..., description="用户名称", example="小林")
    nickname: str = Field(..., description="用户昵称", example="小林")
    phone: str = Field(..., description="手机号码", example="13800138000")
    email: str = Field(..., description="邮箱", example="zhangsan@example.com")
    password: str = Field(..., description="密码", example="<PASSWORD>")
    sex: Optional[int] = Field(None, description="性别（0男 1女 2未知）", example=0)
    deptId: Optional[int] = Field(None, description="部门ID", example=1)
    status: Optional[int] = Field(None, description="用户状态（1正常 0停用）", example=1)
    remark: Optional[str] = Field(None, description="备注", example="备注")


class Update(BaseModel):
    id: Optional[int] = Field(0, description="用户ID", example=0)
    username: str = Field(None, description="用户名称", example="小林")
    nickname: str = Field(None, description="用户昵称", example="小林")
    phone: str = Field(None, description="手机号码", example="13800138000")
    email: str = Field(None, description="邮箱", example="zhangsan@example.com")
    sex: Optional[int] = Field(None, description="性别（0男 1女 2未知）", example=0)
    deptId: Optional[int] = Field(None, description="部门ID", example=1)
    status: Optional[int] = Field(None, description="用户状态（1正常 0停用）", example=1)
    remark: Optional[str] = Field(None, description="备注", example="备注")

class RoleIds(BaseModel):
    userId: int = Field(..., description="用户ID", example=0)

class ResetPassword(BaseModel):
    id: int = Field(..., description="用户ID", example=0)
    password: str = Field(..., description="密码", example="<PASSWORD>")

class AssignRole(BaseModel):
    id: int = Field(..., description="用户ID", example=0)
    roleIds: List[int] = Field(..., description="角色ID列表", example=[1, 2])

class Avatar(BaseModel):
    id: int = Field(..., description="用户ID", example=0)
    avatar: Optional[str] = Field(None, description="用户头像", example="base64编码的图片数据")