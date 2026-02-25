# 导入操作系统模块
import os
# 导入系统模块
import sys
# 导入时间模块
import time
# 导入socket模块
import socket
# 导入系统运行信息模块
import psutil
# 导入平台模块
import platform
# 获取日期时间模块
from datetime import datetime
# 导入Flask 模块
from flask import current_app

# 服务操作工具类
class ServerUtils:
    @staticmethod
    def get_host_ip() -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
        
    @staticmethod
    def Cpu() -> dict:
        scputimes = psutil.cpu_times_percent(interval=1)
        cpu_num = psutil.cpu_count(logical=True)
        used = getattr(scputimes, 'user', 0)
        sys_usage = getattr(scputimes, 'system', 0)
        free = getattr(scputimes, 'idle', 0)
        return {
            "cpuNum": cpu_num,
            "used": round(used, 2),
            "sys": round(sys_usage, 2),
            "free": round(free, 2)
        }
    
    @staticmethod
    def Memory() -> dict:
        memory = psutil.virtual_memory()
        return {
            "total": f"{memory.total / (1024 ** 3):.2f}",
            "used": f"{memory.used / (1024 ** 3):.2f}",
            "free": f"{memory.free / (1024 ** 3):.2f}",
            "usage": round(memory.percent, 2)
        }
    
    @staticmethod
    def Sys() -> dict:
        try:
            user_dir = current_app.extensions['flaskowl'].proot
        except Exception:
            user_dir = os.getcwd()
        return {
            "computerName": platform.node(),
            "osName": platform.system(),
            "computerIp": ServerUtils.get_host_ip(),
            "osArch": platform.machine(),
            "userDir": user_dir
        }
    
    @staticmethod
    def Runtime() -> dict:
        current_process = psutil.Process(os.getpid())
        start_time_ts = current_process.create_time()
        start_time = datetime.fromtimestamp(start_time_ts).strftime("%Y-%m-%d %H:%M:%S")
        uptime = datetime.now() - datetime.fromtimestamp(start_time_ts)
        days, rem1 = divmod(int(uptime.total_seconds()), 86400)
        hours, rem2 = divmod(rem1, 3600)
        minutes, _ = divmod(rem2, 60)
        run_time = f"{days}天{hours}小时{minutes}分钟"
        # Python运行时内存信息
        proc = psutil.Process(os.getpid())
        memory = proc.memory_info()
        total = memory.rss / (1024 * 1024)
        system_memory = psutil.virtual_memory()
        free = system_memory.available / (1024 * 1024)
        total_system_memory_mb = system_memory.total / (1024 * 1024)
        usage_percent = (total / total_system_memory_mb) * 100 if total_system_memory_mb > 0 else 0
        return {
            "name": platform.python_implementation(),
            "version": platform.python_version(),
            "home": sys.executable or sys.prefix,
            "startTime": start_time,
            "inputArgs": " ".join(sys.argv) if sys.argv else "",
            "runTime": run_time,
            "total": round(total, 2),
            "used": round(total, 2),
            "free": round(free, 2),
            "usage": round(usage_percent, 2)
        }
    
    @staticmethod
    def Disk() -> dict:
        sys_files = []
        for part in psutil.disk_partitions():
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            try:
                usage = psutil.disk_usage(part.mountpoint)
                sys_files.append({
                    "dirName": part.mountpoint,
                    "sysTypeName": part.fstype,
                    "typeName": part.device,
                    "total": f"{usage.total / (1024 ** 3):.2f} GB",
                    "free": f"{usage.free / (1024 ** 3):.2f} GB",
                    "used": f"{usage.used / (1024 ** 3):.2f} GB",
                    "usage": usage.percent,
                })
            except (PermissionError, OSError):
                continue
        return sys_files
