# 导入数据库事件监听
from sqlalchemy import event
# 导入时间模块
from datetime import datetime
# 导入数据库对象
from app.common.extension import db


class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    
    def to_dict(self, exclude=None, camel_case=True):
        """将模型转换为字典
        
        :param exclude: 排除的字段列表
        :param camel_case: 是否转换为小驼峰命名，默认开启
        :return: 字典格式的模型数据
        """
        if exclude is None:
            exclude = []
        result = {}
        for column in self.__table__.columns:
            if column.name in exclude:
                continue
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            # 排除隐私相关的字段
            if column.name in ['password']:
                continue
            field_name = column.name
            if camel_case:
                field_name = self._to_camel_case(field_name)
            result[field_name] = value
        return result
    
    def save(self):
        """保存模型"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """删除模型"""
        db.session.delete(self)
        db.session.commit()
        return self
    
    def update(self, **kwargs):
        """更新模型"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self
    
    @classmethod
    def get_by_id(cls, id):
        """根据ID获取模型"""
        return cls.query.get(id)
    
    @classmethod
    def get_by_ids(cls, ids):
        """根据ID列表获取模型"""
        return cls.query.filter(cls.id.in_(ids)).all()
    
    @classmethod
    def get_all(cls):
        """获取所有模型"""
        return cls.query.all()
    
    @classmethod
    def get_by_condition(cls, **kwargs):
        """根据条件查询模型"""
        query = cls.query
        for key, value in kwargs.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key) == value)
        return query.all()
    
    @classmethod
    def get_paginated(cls, page=1, per_page=10, **kwargs):
        """分页查询模型"""
        query = cls.query
        for key, value in kwargs.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key) == value)
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @classmethod
    def delete_by_ids(cls, ids):
        """根据ID列表删除模型"""
        return cls.query.filter(cls.id.in_(ids)).delete(synchronize_session=False)
    
    def _to_camel_case(self, snake_str):
        """将下划线命名转换为小驼峰命名"""
        components = snake_str.split('_')
        # 第一个单词保持小写，后续单词首字母大写
        return components[0] + ''.join(x.capitalize() for x in components[1:])


# 定义审计字段的混入类
class AuditMixin:
    """审计字段混入类，用于为模型添加创建者、创建时间、更新者、更新时间字段"""
    create_by = db.Column(db.String(64), nullable=True, comment='创建者')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_by = db.Column(db.String(64), nullable=True, comment='更新者')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


# 为所有包含审计字段的模型添加自动填充功能
@event.listens_for(db.Model, 'before_insert', propagate=True)
def auto_insert(mapper, connection, target):
    # 检查模型是否包含审计字段
    if hasattr(target, 'create_by') and hasattr(target, 'create_time'):
        try:
            # 获取当前请求上下文
            from flask import g
            identity = getattr(g, 'current_user', None)
            if identity:
                target.create_by = identity
        except RuntimeError:
            # 非请求上下文（如 CLI、定时任务），可选留空或设为系统用户
            target.create_by = "system"
        target.create_time = datetime.now()

@event.listens_for(db.Model, 'before_update', propagate=True)
def auto_update(mapper, connection, target):
    # 检查模型是否包含审计字段
    if hasattr(target, 'update_by') and hasattr(target, 'update_time'):
        try:
            # 获取当前请求上下文
            from flask import g
            identity = getattr(g, 'current_user', None)
            if identity:
                target.update_by = identity
        except RuntimeError:
            target.update_by = "system"
        target.update_time = datetime.now()
