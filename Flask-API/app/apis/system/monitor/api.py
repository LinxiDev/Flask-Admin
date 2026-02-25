# 导入Flask 蓝本模块
from flask import Blueprint
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入统一返回响应模块
from app.common.responses import success
# 导入记录日志模块
from app.common.decorator import record_log
# 导入权限检查装饰器
from app.common.decorator import hasPermi

# 创建公共实现模块
bp = Blueprint('monitor', __name__,url_prefix="/monitor")

# 服务监控
@bp.route('/server', methods=['GET'])
@siwa.doc(tags=["系统监控"], summary="服务监控")
@hasPermi("sys:monitor:query")
def server():
    return success(Services.server())