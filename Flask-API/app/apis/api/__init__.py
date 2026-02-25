# 导入Flask 蓝本模块
from flask import Blueprint

# 在模块中导出蓝图
from .linxiapi import linapi_bp
from .question import question_bp

# 注册蓝图
lin_bp = Blueprint('lin', __name__)
lin_bp.register_blueprint(linapi_bp)
lin_bp.register_blueprint(question_bp)
