# 导入 typing 的 Optional 和 List 用于类型提示
from typing import Optional, List
# 导入 Pydantic 的 BaseModel 和 Field 用于数据模型定义
from pydantic import BaseModel, Field, field_validator


class Query(BaseModel):
    name: Optional[str] = Field(None, description="角色名称", example="管理员")
    code: Optional[str] = Field(None, description="角色编码", example="admin")
    status: Optional[int] = Field(None, description="用户状态（0正常 1停用）", example=0)
    pageSize: Optional[int] = Field(10, description="每页数量", example=10)
    currentPage: Optional[int] = Field(1, description="当前页", example=1)

    # 将空字符串转换为None
    @field_validator('name', 'status','code',mode='before')
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v
    
class Create(BaseModel):
    name: str = Field(..., description="角色名称", example="管理员")
    code: str = Field(..., description="角色编码", example="admin")
    remark: Optional[str] = Field(None, description="备注", example="管理员角色")

class Update(BaseModel):
    id: Optional[int] = Field(0, description="角色ID", example=0)
    name: str = Field(None, description="角色名称", example="管理员")
    code: str = Field(None, description="角色编码", example="admin")
    remark: Optional[str] = Field(None, description="备注", example="管理员角色")
    status: int = Field(None, description="用户状态（1正常 0停用）", example=1)

class RoleMenuId(BaseModel):
    id: int = Field(..., description="角色ID", example=1)


class assignMenu(BaseModel):
    id: int = Field(..., description="角色ID", example=1)
    menuIds: List[int] = Field(..., description="菜单ID列表", example=[1,2,3])
