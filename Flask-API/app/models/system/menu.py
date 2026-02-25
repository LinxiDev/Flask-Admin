# 导入数据库对象
from app.common.extension import db
# 导入基础模型类
from app.models.base import BaseModel

class SysMenu(BaseModel):
    __tablename__ = 'sys_menu'

    parent_id = db.Column(db.BigInteger, default=0, comment='父菜单ID')
    name = db.Column(db.String(50), comment='路由名称')
    title = db.Column(db.String(64), nullable=False, comment='菜单名称/标题')
    path = db.Column(db.String(128), comment='路由路径')
    component = db.Column(db.String(128), comment='组件路径')
    auths = db.Column(db.String(100), comment='权限标识')
    icon = db.Column(db.String(64), default='', comment='菜单图标')
    rank = db.Column(db.Integer, default=0, comment='排序')
    type = db.Column(db.SmallInteger, nullable=False, default=0, comment='菜单类型 (0:目录/页面 1:菜单 2:接口 3:按钮 4:外链)')
    show_link = db.Column(db.Boolean, default=True, comment='是否在菜单中显示')
    frame_src = db.Column(db.String(255), comment='内嵌 链接')
    keep_alive = db.Column(db.Boolean, default=True, comment='缓存标识 (0:不缓存 1:缓存)')
    redirect = db.Column(db.String(128), comment='重定向路径')
    extra_icon = db.Column(db.String(100), comment='额外图标')
    enter_transition = db.Column(db.String(100), comment='进入过渡动画')
    leave_transition = db.Column(db.String(100), comment='离开过渡动画')
    active_path = db.Column(db.String(128), comment='激活路径')
    frame_loading = db.Column(db.Boolean, default=True, comment='内嵌加载状态 (0:不加载 1:加载)')
    hidden_tag = db.Column(db.Boolean, default=False, comment='隐藏标签 (0:不隐藏 1:隐藏)')
    fixed_tag = db.Column(db.Boolean, default=False, comment='固定标签 (0:不固定 1:固定)')
    show_parent = db.Column(db.Boolean, default=False, comment='显示父菜单 (0:不显示 1:显示)')