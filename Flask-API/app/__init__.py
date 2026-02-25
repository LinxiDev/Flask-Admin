# 第三方库导入
# Flask静态文件处理模块
from flask import send_file

# 本地应用/库导入
# 导入Flask应用实例
from app.core import app
# 导入扩展模块和配置
from app.common.extension import db, jwt, cors, siwa, Config
# 导入全局异常处理器注册函数
from app.common.exceptions import register_exception_handlers

# 导出配置对象
__all__ = ['app', 'Config', 'db', 'jwt', 'cors', 'siwa']

# 注册全局异常处理器
register_exception_handlers(app)

# 配置数据库连接信息
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["SQLALCHEMY_ECHO"] = Config.DEBUG
# 配置数据库连接池信息
app.config["SQLALCHEMY_POOL_SIZE"] = Config.SQLALCHEMY_POOL_SIZE
app.config["SQLALCHEMY_MAX_OVERFLOW"] = Config.SQLALCHEMY_MAX_OVERFLOW
app.config["SQLALCHEMY_POOL_TIMEOUT"] = Config.SQLALCHEMY_POOL_TIMEOUT
# 配置JWT认证信息
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = Config.JWT_REFRESH_TOKEN_EXPIRES
# 配置接口文档授权
app.config["SIWA_USER"] = Config.SIWA_USER
app.config["SIWA_PASSWORD"]=Config.SIWA_PASSWORD

# 初始化扩展模块
db.init_app(app)
jwt.init_app(app)
cors.init_app(app)
siwa.init_app(app)

# 注册蓝图模块
# 导入认证相关蓝图
from app.apis.auth import auth_bp
# 导入通用相关蓝图
from app.apis.comm import comm_bp
# 导入系统相关蓝图
from app.apis.system import syst_bp
# 导入开发API蓝图
from app.apis.api import lin_bp

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(comm_bp, url_prefix='/api/comm')
app.register_blueprint(syst_bp, url_prefix='/api/sys')
app.register_blueprint(lin_bp, url_prefix='/api/v1/lin')

# 首页
@app.route('/')
@app.route('/api')
@siwa.doc(summary="接口首页", tags=["首页"])
def index():
    return f"⛱欢迎使用{Config.NAME} V{Config.VERSION}!"

# 图标
@app.route('/favicon.ico')
def favicon():
    return send_file('../assets/favicon.ico', mimetype='image/vnd.microsoft.icon')