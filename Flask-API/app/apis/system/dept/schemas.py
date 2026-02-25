# 导入 Pydantic 的 BaseModel 和 Field 用于数据模型定义
from pydantic import BaseModel, Field, field_validator
# 导入 typing 的 Optional 和 List 用于类型提示
from typing import Optional


class Query(BaseModel):
    name: Optional[str] = Field(None, description="部门名称", example="技术部")
    status: Optional[int] = Field(None, description="部门状态（0正常 1停用）", example=0)

    # 将空字符串转换为None
    @field_validator('name', 'status',mode='before')
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v
    
class Create(BaseModel):
    parentId: Optional[int] = Field(0, description="父部门id", example=0)
    name: str = Field(..., description="部门名称", example="技术部")
    sort: Optional[int] = Field(0, description="显示顺序", example=1)
    leader: Optional[str] = Field(None, description="负责人", example="张三")
    phone: Optional[str] = Field(None, description="联系电话", example="13800138000")
    email: Optional[str] = Field(None, description="邮箱", example="zhangsan@example.com")
    status: Optional[int] = Field(None, description="部门状态（1正常 0停用）", example=0)
    remark: Optional[str] = Field(None, description="备注", example="研发部门")

class Update(Create):
    id: Optional[int] = Field(0, description="部门ID", example=0)