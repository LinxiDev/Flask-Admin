# 标准库导入
# 用于IP地址处理
from ipaddress import ip_address
# 用于日期时间处理
from datetime import datetime

# 第三方库导入
# 网络请求模块
import requests
# 日志记录模块
from loguru import logger
# UA请求头解析模块
from user_agents import parse

class CommonUtils:
    # 请求信息工具类 - 获取IP、地址、系统、浏览器等信息
    @staticmethod
    def get_request_info(ip,ua_str) -> dict:
        if ip_address(ip.strip()).is_private:
            address = '内网IP'
        else:
            # 查询外网IP归属地
            try:
                ipJson = requests.get(f'https://whois.pconline.com.cn/ipJson.jsp?json=true&ip={ip}').json()
                address = ipJson.get('pro') + ' ' + ipJson.get('city')
            except Exception as e:
                logger.error(f"查询外网IP归属地异常: {str(e)}")
                address = '未知 位置'
        ua = parse(ua_str)
        system = f"{ua.os.family} {ua.os.version_string or ""}"
        browser = F"{ua.browser.family} {ua.browser.version_string or ""}"
        return address, system, browser
