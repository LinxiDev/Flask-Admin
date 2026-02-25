# 导入Flask 蓝本模块
from flask import Blueprint
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入统一返回响应模块
from app.common.responses import page,success
# 导入日志装饰器
from app.common.decorator import record_log
# 导入权限检查装饰器
from app.common.decorator import hasPermi
# 导入数据模型定义
from .schemas import LoginQuery,OperQuery,SysQuery

bp = Blueprint('logs', __name__,url_prefix="/logs")

@bp.route('/loginLogs', methods=['POST'])
@siwa.doc(body=LoginQuery,tags=["日志管理"], summary="日志列表")
@hasPermi("sys:loginlog:query")
def login_list(body: LoginQuery):
    return page(*Services.login_list(body))

# 批量删除登陆日志
@bp.route("/loginLogs/<path:ids>",methods=['DELETE'])
@siwa.doc(tags=["日志管理"], summary="批量删除登陆日志")
@record_log(module="日志管理",summary="批量删除登陆日志")
@hasPermi("sys:loginlog:remove")
def delete_login_logs(ids: int):
    return success(Services.delete_login_logs(ids))

# 清空登陆日志
@bp.route("/loginLogs/clear",methods=['DELETE'])
@siwa.doc(tags=["日志管理"], summary="清空登陆日志")
@record_log(module="日志管理",summary="清空登陆日志")
@hasPermi("sys:loginlog:remove")
def clear_login_logs():
    return success(Services.clear_login_logs())


@bp.route('/operateLogs', methods=['POST'])
@siwa.doc(body=OperQuery,tags=["日志管理"], summary="操作日志列表")
@hasPermi("sys:operatelog:query")
def operate_list(body: OperQuery):
    return page(*Services.operate_list(body))

# 批量删除操作日志
@bp.route("/operateLogs/<path:ids>",methods=['DELETE'])
@siwa.doc(tags=["日志管理"], summary="批量删除操作日志")
@record_log(module="日志管理",summary="批量删除操作日志")
@hasPermi("sys:operatelog:remove")
def delete_operate_logs(ids: int):
    return success(Services.delete_operate_logs(ids))

# 清空操作日志
@bp.route("/operateLogs/clear",methods=['DELETE'])
@siwa.doc(tags=["日志管理"], summary="清空操作日志")
@record_log(module="日志管理",summary="清空操作日志")
@hasPermi("sys:operatelog:remove")
def clear_operate_logs():
    return success(Services.clear_operate_logs())


@bp.route('/systemLogs', methods=['POST'])
@siwa.doc(body=SysQuery,tags=["日志管理"], summary="系统日志列表")
@hasPermi("sys:systemlog:query")
def system_list(body: SysQuery):
    return page(*Services.system_list(body))

# 根据ID查询系统日志
@bp.route('/systemLogs/<int:id>', methods=['GET'])
@siwa.doc(tags=["日志管理"], summary="根据ID查询系统日志")
@hasPermi("sys:systemlog:query")
def system_detail(id: int):
    return success(Services.system_detail(id))


@bp.route('/systemLogs/<path:ids>', methods=['DELETE'])
@siwa.doc(tags=["日志管理"], summary="批量删除系统日志")
@record_log(module="日志管理",summary="批量删除系统日志")
@hasPermi("sys:systemlog:remove")
def delete_system_logs(ids: int):
    return success(Services.delete_system_logs(ids))


@bp.route('/systemLogs/clear', methods=['DELETE'])
@siwa.doc(tags=["日志管理"], summary="清空系统日志")
@record_log(module="日志管理",summary="清空系统日志")
@hasPermi("sys:systemlog:remove")
def clear_system_logs():
    return success(Services.clear_system_logs())