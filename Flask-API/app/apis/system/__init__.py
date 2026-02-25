# 导入Flask 蓝本模块
from flask import Blueprint

# 在模块中导出蓝图
from .user import user_bp
from .role import role_bp
from .menu import menu_bp
from .dept import dept_bp
from .logs import logs_bp
from .monitor import moni_bp

syst_bp = Blueprint('system', __name__)
syst_bp.register_blueprint(user_bp)
syst_bp.register_blueprint(role_bp)
syst_bp.register_blueprint(menu_bp)
syst_bp.register_blueprint(dept_bp)
syst_bp.register_blueprint(logs_bp)
syst_bp.register_blueprint(moni_bp)