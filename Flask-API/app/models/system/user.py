# 导入数据库对象
from app.common.extension import db
# 导入基础模型类和审计混入类
from app.models.base import BaseModel, AuditMixin


class SysUser(BaseModel, AuditMixin):
    __tablename__ = 'sys_user'
    
    username = db.Column(db.String(30), nullable=False, comment='用户账号')
    nickname = db.Column(db.String(30), nullable=False, comment='用户昵称')
    sex = db.Column(db.SmallInteger, default=1, comment='性别(0女 1男 2未知)')
    password = db.Column(db.String(100), comment='密码')
    avatar = db.Column(db.String(255), comment='用户头像')
    phone = db.Column(db.String(20), comment='手机号码')
    status = db.Column(db.SmallInteger, default=1, comment='账号状态(0停用 1正常)')
    email = db.Column(db.String(128), comment='用户邮箱')
    deleted = db.Column(db.SmallInteger, default=0, comment='删除标志(0代表存在 1代表删除)')
    remark = db.Column(db.String(255), comment='备注')

    # 定义与角色的多对多关系
    roles = db.relationship('SysRole', secondary='sys_user_role', backref='users')

    dept = db.relationship('SysDept', secondary='sys_user_dept', backref='users')

    # 根据用户名查询
    @staticmethod
    def get_by_username(username: str):
        return SysUser.query.filter_by(username=username, deleted=0).first()


class SysUserRole(db.Model):
    __tablename__ = 'sys_user_role'

    user_id = db.Column(db.BigInteger, db.ForeignKey('sys_user.id'), primary_key=True, comment='用户ID')
    role_id = db.Column(db.BigInteger, db.ForeignKey('sys_role.id'), primary_key=True, comment='角色ID')

    def save(self):
        db.session.add(self)
        db.session.commit()
