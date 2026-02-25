# 导入 Pydantic 的 BaseModel 和 Field 用于数据模型定义
from pydantic import BaseModel, Field

# 查询订单
class QueryModel(BaseModel):
    page: int = Field(default=1, title="当前页码")
    size: int = Field(default=8, title="一页的数量大小", ge=8, le=100)
    keyword: str = None

# 获取订单的信息
class INFOModel(BaseModel):
    order_id: str

# 获取创建订单消息
class PayOrderModel(BaseModel):
    order_id: str
    money: float
    product: str

# 获取回调订单信息
class BackModel(BaseModel):
    back_msg: str