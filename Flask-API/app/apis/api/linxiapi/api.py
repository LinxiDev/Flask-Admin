# 导入Flask 蓝本模块
from flask import Blueprint,request
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入统一返回响应模块
from app.common.responses import success,fail
# 导入数据模型定义
from .schemas import *

# 创建认证蓝图
bp = Blueprint('lin', __name__)


@bp.route('/paylist', methods=['GET'])
@siwa.doc(query=QueryModel,tags=["赞赏支付"], summary="订单查询")
def login(query: QueryModel):
    return success(Services.pagelist(query))

@bp.route('/payinfo', methods=['GET'])
@siwa.doc(query=INFOModel,tags=["赞赏支付"], summary="订单信息")
def info(query: INFOModel):
    return success(Services.info(query))

@bp.route('/pay', methods=['POST'])
@siwa.doc(body=PayOrderModel,tags=["赞赏支付"], summary="创建订单")
def pay(body: PayOrderModel):
    return success(Services.pay(body))

@bp.route('/back', methods=['POST'])
@siwa.doc(body=BackModel,tags=["赞赏支付"], summary="回调订单")
def back(body: BackModel):
    return success(Services.back(body))