# 导入系统模块
import os
# 导入UUID
import uuid
# 导入日志模块
from loguru import logger
# 导入日期时间模块
from datetime import datetime
# 导入Flask 返回文件信息
from flask import send_from_directory
# 导入统一响应
from app.common.exceptions import APIException
# 导入数据模型

class Services:
    @staticmethod
    def upload(files: dict):
        fileList = files.get('file',[])
        if not fileList:
            raise APIException(msg="请选择文件")
        date_dir = datetime.now().strftime('%Y/%m/%d')
        result = []
        for file in fileList:
            new_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            # 保存文件
            target_dir = os.path.join("upload", date_dir)
            os.makedirs(target_dir, exist_ok=True)
            file.save(os.path.join(target_dir, new_filename))
            logger.info(f"文件 {file.filename} 已保存为 {new_filename}")
            result.append({
                "filename": file.filename,
                "new_filename": new_filename,
                "url": f"/api/comm/upload/{date_dir}/{new_filename}"
            })
        return result
        
    
    @staticmethod
    def download(fileName: str):
        file_path = os.path.join("upload", fileName)
        # 判断文件夹下面是否存在图片
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory("../../upload/", fileName)
        else:
            return APIException("资源不存在")

