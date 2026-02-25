# 导入Flask 蓝本模块
from flask import Blueprint
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入统一返回响应模块
from app.common.responses import success,page
# 导入数据模型定义
from .schemas import Query, Create, Update,RoleIds,ResetPassword,AssignRole,Avatar
# 导入日志模块
from app.common.decorator import record_log
# 导入权限检查装饰器
from app.common.decorator import hasPermi

# 创建用户蓝图
bp = Blueprint('user', __name__,url_prefix="/user")

@bp.route('/list', methods=['GET'])
@siwa.doc(query=Query,tags=["用户管理"], summary="用户列表")
@hasPermi("sys:user:query")
def list(query: Query):
    return page(Services.list(query))


@bp.route('', methods=['POST'])
@siwa.doc(body=Create,tags=["用户管理"], summary="新增用户")
@record_log(module="系统管理", summary="系统管理-新增用户")
@hasPermi("sys:user:add")
def add(body: Create):
    return success(Services.add(body))

@bp.route('/<path:ids>', methods=['DELETE'])
@siwa.doc(tags=["用户管理"], summary="删除用户")
@record_log(module="系统管理", summary="系统管理-删除用户")
@hasPermi("sys:user:remove")
def delete(ids: int):
    return success(Services.delete(ids))

@bp.route('', methods=['PUT'])
@siwa.doc(body=Update,tags=["用户管理"], summary="编辑用户")
@record_log(module="系统管理", summary="系统管理-编辑用户")
@hasPermi("sys:user:edit")
def edit(body: Update):
    return success(Services.edit(body))

# 根据用户ID获取对应的角色id列表
@bp.route('/roleIds', methods=['GET'])
@siwa.doc(query=RoleIds,tags=["用户管理"], summary="获取当前用户角色列表")
@hasPermi("sys:user:query")
def get_roleIds(query: RoleIds):
    return success(Services.get_roleIds(query.userId))

# 重置用户密码
@bp.route('/resetPassword', methods=['PUT'])
@siwa.doc(body=ResetPassword,tags=["用户管理"], summary="重置用户密码")
@record_log(module="系统管理", summary="系统管理-重置用户密码")
@hasPermi("sys:user:resetPwd")
def change_password(body: ResetPassword):
    return success(Services.change_password(body))

# 分配权限
@bp.route('/assignRole', methods=['PUT'])
@siwa.doc(body=AssignRole,tags=["用户管理"], summary="分配权限")
@record_log(module="系统管理", summary="系统管理-分配权限")
@hasPermi("sys:user:edit")
def assign_role(body: AssignRole):
    return success(Services.assign_role(body))

@bp.route('/uploadAvatar', methods=['PUT'])
@siwa.doc(body=Avatar,tags=["用户管理"], summary="上传头像")
@record_log(module="系统管理", summary="系统管理-上传头像")
@hasPermi("sys:user:edit")
def upload_avatar(body: Avatar):
    return success(Services.upload_avatar(body))