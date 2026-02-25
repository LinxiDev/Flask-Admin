# 导入 Pydantic 的 BaseModel 和 Field 用于数据模型定义
from typing import Optional
from pydantic import BaseModel, Field


# 题库查询接口
class QueryModel(BaseModel):
    id: int = Field(None, title="ID", description="唯一标识符")
    question: str = Field(None, title="问题", description="问题内容")

# 题库上传接口
class UploadModel(BaseModel):
    id: int = Field(None, title="ID", description="唯一标识符")
    question: str = Field(..., title="问题", description="问题内容")
    answer: str = Field(..., title="答案", description="答案内容")
    remark: str = Field(None, title="备注", description="备注信息")