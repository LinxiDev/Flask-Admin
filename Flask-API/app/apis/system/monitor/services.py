# 导入系统服务工具类
from app.utils import ServerUtils

class Services:
    @staticmethod
    def server() -> dict:
        return {
            "cpu": ServerUtils.Cpu(),
            "mem": ServerUtils.Memory(),
            "sys": ServerUtils.Sys(),
            "runtime": ServerUtils.Runtime(),
            "sysFiles": ServerUtils.Disk(),
        }
