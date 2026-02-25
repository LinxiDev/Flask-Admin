# 项目基本配置
class Config:
    NAME: str = 'Flask-API'
    VERSION: str = '1.0.0'
    HOST: str = '0.0.0.0'
    PORT: int = 80
    DEBUG: bool = True

    # 数据库配置
    DB_HOST: str = 'mysql2.sqlpub.com'
    DB_PORT: int = 3307
    DB_USER: str = 'linxidev'
    DB_PASSWORD: str = 'xxxxxx'
    DB_NAME: str = 'linxidev'
    SQLALCHEMY_DATABASE_URI: str = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    # 数据库连接池配置
    # 连接池大小
    SQLALCHEMY_POOL_SIZE: int = 10
    # 连接池达到最大值后可以创建的连接数
    SQLALCHEMY_MAX_OVERFLOW: int = 5
    # 设定连接池获取连接的超时时间（秒），默认是10
    SQLALCHEMY_POOL_TIMEOUT: int = 30
    # 多少秒后自动回收连接（即关闭）
    # SQLALCHEMY_POOL_RECYCLE: int = 1800

    # JWT认证配置
    JWT_SECRET_KEY: str = 'linxi.xxxxxx'
    # 有效期2小时
    JWT_ACCESS_TOKEN_EXPIRES: int = 60 * 60 * 2
    # 有效期30天
    JWT_REFRESH_TOKEN_EXPIRES: int = 60 * 60 * 24 * 30

    # 跨域配置
    CORS_ORIGINS: list = ["*"]

    # 接口文档配置
    SIWA_USER: str = 'linxi'
    SIWA_PASSWORD: str = 'linxi.xxxxxxx'

    # 微信公众号配置
    WX_APPID: str = 'wxd0eef24ce7b830c6'
    WX_SECRET: str = 'xxxxxx'

    