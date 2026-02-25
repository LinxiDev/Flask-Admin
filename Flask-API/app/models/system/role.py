# 导入数据库对象
from app.common.extension import db
# 导入基础模型类和审计混入类
from app.models.base import BaseModel, AuditMixin

class SysRole(BaseModel, AuditMixin):
    __tablename__ = 'sys_role'
    
    name = db.Column(db.String(30), nullable=False, comment='角色名称')
    code = db.Column(db.String(30), nullable=False, comment='角色编码')
    status = db.Column(db.SmallInteger, default=1, comment='角色状态(0禁用 1正常)')
    deleted = db.Column(db.SmallInteger, default=0, comment='删除标志(0代表存在 1代表删除)')
    remark = db.Column(db.String(255), comment='备注')

    # 定义角色与菜单的多对多关系
    menus = db.relationship('SysMenu', secondary='sys_role_menu', backref='roles')


class SysRoleMenu(db.Model):
    __tablename__ = 'sys_role_menu'

    role_id = db.Column(db.BigInteger, db.ForeignKey('sys_role.id'), primary_key=True, comment='角色ID')
    menu_id = db.Column(db.BigInteger, db.ForeignKey('sys_menu.id'), primary_key=True, comment='菜单ID')
