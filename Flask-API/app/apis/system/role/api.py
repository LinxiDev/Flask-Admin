# 导入Flask 蓝本模块
from flask import Blueprint
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入统一返回响应模块
from app.common.responses import success,page
# 导入数据模型定义
from .schemas import Query,Create,Update,RoleMenuId,assignMenu
# 导入日志模块
from app.common.decorator import record_log
# 导入权限检查装饰器
from app.common.decorator import hasPermi


# 创建角色蓝图
bp = Blueprint('role', __name__,url_prefix="/role")

@bp.route('/list', methods=['GET'])
@siwa.doc(query=Query,tags=["角色管理"], summary="角色列表")
@hasPermi("sys:role:query")
def list(query: Query):
    return page(Services.list(query))

@bp.route('/listAll', methods=['GET'])
@siwa.doc(tags=["角色管理"], summary="角色全部列表")
@hasPermi("sys:role:query")
def listAll():
    return success(Services.listAll())

@bp.route('', methods=['POST'])
@siwa.doc(body=Create,tags=["角色管理"], summary="新增角色")
@record_log(module="系统管理", summary="系统管理-新增角色")
@hasPermi("sys:role:add")
def add(body: Create):
    return success(Services.add(body))

@bp.route('/<path:ids>', methods=['DELETE'])
@siwa.doc(tags=["角色管理"], summary="删除角色")
@record_log(module="系统管理", summary="系统管理-删除角色")
@hasPermi("sys:role:remove")
def delete(ids: int):
    return success(Services.delete(ids))

@bp.route('', methods=['PUT'])
@siwa.doc(body=Update,tags=["角色管理"], summary="编辑角色")
@record_log(module="系统管理", summary="系统管理-编辑角色")
@hasPermi("sys:role:edit")
def edit(body: Update):
    return success(Services.edit(body))

@bp.route('/roleMenu', methods=['GET'])
@siwa.doc(tags=["角色管理"], summary="获取角色菜单")
@hasPermi("sys:role:query")
def getRoleMenu():
    return success(Services.getRoleMenu())


# 获取角色菜单权限IDS
@bp.route('/getRoleMenuIds', methods=['GET'])
@siwa.doc(query=RoleMenuId,tags=["角色管理"], summary="获取角色权限IDS")
@hasPermi("sys:role:query")
def getRoleMenuIds(query: RoleMenuId):
    return success(Services.getRoleMenuIds(query.id))


# 分配角色菜单权限
@bp.route('/assignMenu', methods=['POST'])
@siwa.doc(body=assignMenu,tags=["角色管理"], summary="分配角色权限")
@record_log(module="系统管理", summary="系统管理-分配角色权限")
@hasPermi("sys:role:edit")
def saveAssignMenu(body: assignMenu):
    return success(Services.assignMenu(body))
