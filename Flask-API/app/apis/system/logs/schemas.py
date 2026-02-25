# 导入 Pydantic 的 BaseModel 和 Field 用于数据模型定义
from pydantic import BaseModel, Field,field_validator
# 导入 typing 的 Optional 和 List 用于类型提示
from typing import Optional


class LoginQuery(BaseModel):
    username: Optional[str] = Field(None, description="用户名", example="admin")
    status: Optional[int] = Field(None, description="登陆状态（1成功 0失败）", example=1)
    loginTime: Optional[list[str]] = Field(None, description="登陆时间", example=["2023-01-01 00:00:00","2023-01-02 00:00:00"])
    pageSize: Optional[int] = Field(10, description="每页数量", example=10)
    currentPage: Optional[int] = Field(1, description="当前页", example=1)

    # 将空字符串转换为None
    @field_validator('username','status','loginTime',mode='before')
    def empty_str_to_none(cls, v):
        if v == '' or v == []:
            return None
        return v
    

class OperQuery(BaseModel):
    module: Optional[str] = Field(None, description="所属模块", example="认证")
    status: Optional[int] = Field(None, description="操作状态（1成功 0失败）", example=1)
    operatingTime: Optional[list[str]] = Field(None, description="操作时间", example=["2023-01-01 00:00:00","2023-01-02 00:00:00"])
    pageSize: Optional[int] = Field(10, description="每页数量", example=10)
    currentPage: Optional[int] = Field(1, description="当前页", example=1)

    # 将空字符串转换为None
    @field_validator('module','status','operatingTime',mode='before')
    def empty_str_to_none(cls, v):
        if v == '' or v == []:
            return None
        return v
    

class SysQuery(BaseModel):
    module: Optional[str] = Field(None, description="所属模块", example="认证")
    requestTime: Optional[list[str]] = Field(None, description="操作时间", example=["2023-01-01 00:00:00","2023-01-02 00:00:00"])
    pageSize: Optional[int] = Field(10, description="每页数量", example=10)
    currentPage: Optional[int] = Field(1, description="当前页", example=1)

    # 将空字符串转换为None
    @field_validator('module','requestTime',mode='before')
    def empty_str_to_none(cls, v):
        if v == '' or v == []:
            return None
        return v