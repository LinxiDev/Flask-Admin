# 导入数据库对象
from app.common.extension import db
# 导入基础模型类和审计混入类
from app.models.base import BaseModel, AuditMixin
# 导入 SQLAlchemy 混合属性装饰器
from sqlalchemy.ext.hybrid import hybrid_property

class SysDept(BaseModel, AuditMixin):
    __tablename__ = 'sys_dept'
    
    parent_id = db.Column(db.BigInteger, default=0, comment='父部门id')
    dept_name = db.Column(db.String(30), default=None, comment='部门名称')
    order_num = db.Column(db.Integer, default=0, comment='显示顺序')
    leader = db.Column(db.String(20), default=None, comment='负责人')
    phone = db.Column(db.String(20), default=None, comment='联系电话')
    email = db.Column(db.String(128), default=None, comment='邮箱')
    status = db.Column(db.SmallInteger, default=0, comment='部门状态(0正常 1停用)')
    deleted = db.Column(db.SmallInteger, default=0, comment='删除标志(0代表存在 1代表删除)')
    remark = db.Column(db.String(255), comment='备注')

    @hybrid_property
    def status_int(self):
        return 1 if self.status else 0
    
    
class SysUserDept(db.Model):
    __tablename__ = 'sys_user_dept'

    user_id = db.Column(db.BigInteger, db.ForeignKey('sys_user.id'), primary_key=True, comment='用户ID')
    dept_id = db.Column(db.BigInteger, db.ForeignKey('sys_dept.id'), primary_key=True, comment='部门ID')

    def save(self):
        db.session.add(self)
        db.session.commit()