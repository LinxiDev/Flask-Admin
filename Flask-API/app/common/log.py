# 导入系统模块
import sys
# 导入默认日志模块
import logging
# 导入日志模块
from loguru import logger

# 自定义日志处理器
class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

def log(path: str = "logs/app.log", rotation: str = "00:00"):
    """配置日志"""
    logging.basicConfig(handlers=[InterceptHandler(level='INFO')], level='INFO')
    # 配置日志到标准输出流
    logger.configure(handlers=[{"sink": sys.stderr, "level": 'INFO'}])
    # 配置日志到输出到文件
    logger.add(path, retention="7 days", rotation=rotation)