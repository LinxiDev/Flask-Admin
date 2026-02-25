# 第三方库导入
# CORS跨域模块
from flask_cors import CORS
# 接口文档模块
from flask_siwadoc import SiwaDoc
# 数据库ORM模块
from flask_sqlalchemy import SQLAlchemy
# JWT管理模块
from flask_jwt_extended import JWTManager

# 本地应用/库导入
# 项目配置文件
from config import Config
# 日志模块
from app.common.log import log

# 初始化日志模块
log("logs/app.log")
# 初始化数据库对象
db = SQLAlchemy()
# 初始化JWT管理模块
jwt = JWTManager()
# 初始化跨域模块
cors = CORS(origins=Config.CORS_ORIGINS)
# 初始化接口文档模块
siwa = SiwaDoc(title=f"{Config.NAME} V{Config.VERSION}", description=f"{Config.NAME} V{Config.VERSION}接口文档", version=Config.VERSION)
