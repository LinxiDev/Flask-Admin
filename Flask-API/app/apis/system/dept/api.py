# 导入Flask 蓝本模块
from flask import Blueprint
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入统一返回响应模块
from app.common.responses import success
# 导入操作日志装饰器
from app.common.decorator import record_log
# 导入权限检查装饰器
from app.common.decorator import hasPermi
# 导入数据模型定义
from .schemas import Query,Create,Update

# 创建部门蓝图
bp = Blueprint('dept', __name__,url_prefix="/dept")

@bp.route('/list', methods=['GET'])
@siwa.doc(query=Query,tags=["部门管理"], summary="部门列表")
@hasPermi("sys:dept:query")
def list(query: Query):
    return success(Services.list(query))

@bp.route('', methods=['POST'])
@siwa.doc(body=Create,tags=["部门管理"], summary="新增部门")
@record_log(module="系统管理", summary="系统管理-新增部门")
@hasPermi("sys:dept:add")
def add(body: Create):
    return success(Services.add(body))

@bp.route('/<path:ids>', methods=['DELETE'])
@siwa.doc(tags=["部门管理"], summary="删除部门")
@record_log(module="系统管理", summary="系统管理-删除部门")
@hasPermi("sys:dept:remove")
def delete(ids: int):
    return success(Services.delete(ids))

@bp.route('', methods=['PUT'])
@siwa.doc(body=Update,tags=["部门管理"], summary="编辑部门")
@record_log(module="系统管理", summary="系统管理-编辑部门")
@hasPermi("sys:dept:edit")
def edit(body: Update):
    return success(Services.edit(body))
