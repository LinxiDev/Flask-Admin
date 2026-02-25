# 导入Flask 蓝本模块
from flask import Blueprint
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入统一返回响应模块
from app.common.responses import success
# 导入数据模型定义
from .schemas import Query, Create, Update
# 导入日志模块
from app.common.decorator import record_log
# 导入权限检查装饰器
from app.common.decorator import hasPermi


# 创菜单蓝图
bp = Blueprint('menu', __name__,url_prefix="/menu")

@bp.route('', methods=['GET'])
@siwa.doc(query=Query,tags=["菜单管理"], summary="菜单列表")
@hasPermi("sys:menu:query")
def list(query: Query):
    return success(Services.list(query))


@bp.route('', methods=['POST'])
@siwa.doc(body=Create,tags=["菜单管理"], summary="创建菜单")
@record_log(module="系统管理", summary="系统管理-创建菜单")
@hasPermi("sys:menu:add")
def add(body: Create):
    return success(Services.add(body))

@bp.route('', methods=['PUT'])
@siwa.doc(body=Update,tags=["菜单管理"], summary="修改菜单")
@record_log(module="系统管理", summary="系统管理-修改菜单")
@hasPermi("sys:menu:edit")
def update(body:Update):
    return success(Services.edit(body))

# 删除菜单id的菜单
@bp.route('/<int:id>', methods=['DELETE'])
@siwa.doc(tags=["菜单管理"], summary="删除菜单")
@record_log(module="系统管理", summary="系统管理-删除菜单")
@hasPermi("sys:menu:remove")
def delete(id: int):
    return success(Services.delete(id))