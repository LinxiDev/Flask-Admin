# 导入时间模块
from datetime import datetime
# 导入数据库对象
from app.common.extension import db
# 导入基础模型类
from app.models.base import BaseModel

class LinQuestion(BaseModel):
    __tablename__ = 'lin_question'

    id = db.Column(db.BigInteger, primary_key=True, comment='ID')
    qid = db.Column(db.String(50), nullable=False, comment='问题ID')
    question = db.Column(db.String(255), nullable=False, comment='问题标题')
    answer = db.Column(db.Text, nullable=False, comment='答案')
    
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