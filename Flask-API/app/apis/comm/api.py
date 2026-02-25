# 导入Flask 蓝本模块
from flask import Blueprint
# 导入接口实现模块
from .services import Services
# 导入接口文档模块
from app.common.extension import siwa
# 导入统一返回响应模块
from app.common.responses import success
# 导入数据模型
from .schemas import UploadFile
# 导入日志模块
from app.common.decorator import record_log


# 创建公共实现模块
bp = Blueprint('comm', __name__)

# 上传文件
@bp.route('/upload', methods=['POST'])
@siwa.doc(form=UploadFile,files={'file': {"required": True, "single": False}}, tags=["公共接口"], summary="上传文件")
@record_log(module="公共接口", summary="上传文件")
def upload(form: UploadFile, files: dict):
    return success(Services.upload(files))


# 下载文件/预览
@bp.route('/upload/<path:fileName>', methods=['GET'])
@siwa.doc(tags=["公共接口"], summary="下载文件/预览图片")
def download(fileName: str):
    return Services.download(fileName)
