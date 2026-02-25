# 导入数据库操作对象
from app.common.extension import db
# 导入用户模型
from app.models import LinQuestion
# 导入数据模型定义
from .schemas import *
# 导入统一返回响应模块
from app.common.responses import success,fail


# 认证服务
class Services:
    @staticmethod
    def search(query: QueryModel) -> str:
        question = LinQuestion.query.filter(LinQuestion.id == query.id if query.id else True,LinQuestion.question == query.question if query.question else True).first()
        if question:
            return success(question.to_dict())
        else:
            return fail("未查询到该问题!")
        

    @staticmethod
    def upload(body: UploadModel) -> str:
        question = LinQuestion.query.filter(LinQuestion.id == body.id if body.id else True,LinQuestion.question == body.question if body.question else True).first()
        if question:
            question.answer = body.answer
            db.session.add(question)
            db.session.commit()
            return success("更新成功!")
        else:
            return fail("该问题不存在，无法更新!")