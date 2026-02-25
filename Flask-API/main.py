# 导入应用app模块
from app import app, Config


# 启动Flask应用
if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)