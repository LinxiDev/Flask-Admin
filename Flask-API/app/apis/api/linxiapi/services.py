# 导入正则表达式模块
import re
# 导入数据库操作对象
from app.common.extension import db
# 导入时间处理模块
from datetime import datetime,timedelta
# 导入用户模型
from app.models import LinOrders
# 导入数据模型定义
from .schemas import *
# 导入统一返回响应模块
from app.common.responses import success,fail,page


# 认证服务
class Services:
    @staticmethod
    def pagelist(query: QueryModel) -> dict:
        # 更新过期订单
        expired_time = datetime.now() - timedelta(minutes=5)
        LinOrders.query.filter(LinOrders.status == 2,LinOrders.time < expired_time).update({LinOrders.status: 0})
        db.session.commit()
        q = LinOrders.query
        if query.keyword:
            q = q.filter(LinOrders.product.like(f"%{query.keyword}%"))
        data = q.order_by(LinOrders.time.desc(),LinOrders.status.desc()).paginate(query.page, query.size, False)
        return page(data.to_dict(), query.page, query.size)
    
    @staticmethod
    def info(query: INFOModel) -> dict:
        order = LinOrders.query.filter_by(order_id=query.order_id).first()
        if not order:
            return fail("该订单不存在!")
        old_time = order.create_time.timestamp() + 300
        new_time = datetime.now().timestamp()
        tips = ["订单过期，请重新生成订单!", "该订单已完成支付!", "该订单等待支付!", "订单异常，请重新生成订单!"]
        if order.status == 2 and new_time > old_time:
            order.status = 0
            db.session.commit()
            return success(order.to_dict(), tips[order.status])
        if order.status == 2:
            return success({**order.to_dict(), "exp": int(old_time - new_time)}, tips[order.status])
        else:
            return success(order.to_dict(),tips[order.status])
    
    @staticmethod
    def pay(body: PayOrderModel) -> dict:
        existing_order = LinOrders.query.filter(LinOrders.order_id == body.order_id,LinOrders.status == 2).first()
        if existing_order:
            return fail("订单已存在!")
        # 调整金额避免重复
        money = body.money
        while LinOrders.query.filter(LinOrders.money == money,LinOrders.status == 2).first():
            money += 0.01
        body.money = money
        data = LinOrders(**body.model_dump())
        data.status = 2
        db.session.add(data)
        db.session.commit()
        return success(data.to_dict(),"订单创建成功!")
    
    @staticmethod
    def back(body: BackModel) -> dict:
        try:
            money = float(re.findall(r"二维码赞赏到账(.*?)元", body.back_msg)[0])
            order = LinOrders.query.filter(LinOrders.money == money,LinOrders.status == 2).first()
            if order:
                order.status = 1
                db.session.commit()
                return success("订单支付成功!")
            else:
                return fail("该订单不存在!")
        except Exception:
            return fail("参数异常!")