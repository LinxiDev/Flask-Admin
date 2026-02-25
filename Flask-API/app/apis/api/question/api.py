# 导入Flask 蓝本模块
from flask import Blueprint
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入数据模型定义
from .schemas import *

# 创建认证蓝图
bp = Blueprint('question', __name__)


@bp.route('/search', methods=['GET'])
@siwa.doc(query=QueryModel,tags=["题库"], summary="题库查询")
def search(query: QueryModel):
    return Services.search(query)

@bp.route('/upload', methods=['POST'])
@siwa.doc(body=UploadModel,tags=["题库"], summary="题库上传")
def upload(body: UploadModel):
    return Services.upload(body)