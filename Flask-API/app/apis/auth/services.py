# 导入Flask 请求模块
from flask import request
# 导入数据库查询模块
from sqlalchemy.orm import joinedload
# 导入密码工具类
from app.utils import SecurityUtils
# 导入统一响应
from app.common.exceptions import APIException
# 导入用户模型
from app.models import SysUser,SysMenu,SysLoginLog,SysUserRole,SysUserDept

# 存放微信uuid和登陆后的信息
wx_uuid = {}

# 认证服务
class Services:
    @staticmethod
    def login(username: str, password: str) -> dict:
        user = SysUser.query.options(joinedload(SysUser.roles)).filter_by(username=username,deleted=False).first()
        # 获取请求IP
        ip = request.headers.get('X-Real-IP') or request.remote_addr
        # 获取UA信息
        ua = request.headers.get('User-Agent','')
        if not user: 
            # 记录登陆日志
            SysLoginLog.create(username,ip,ua,0)
            raise APIException("用户名或密码错误")
        if user.status == 0: 
            SysLoginLog.create(username,ip,ua,0)
            raise APIException("账户已被禁用")
        if not SecurityUtils.verify_password(password, user.password):
            SysLoginLog.create(username,ip,ua,0)
            raise APIException("用户名或密码错误")
        # 创建Token
        tokens = SecurityUtils.create_tokens(user.username)
        # 获取用户角色信息
        roles = [role.code for role in user.roles if not role.deleted]
        # 有管理员权限则为["*:*:*"]
        perm = ["*:*:*"] if "admin" in roles else [auth.auths for role in user.roles if not role.deleted for auth in role.menus if auth.auths]
        # 记录登陆日志
        SysLoginLog.create(username,ip,ua,1)
        return {
            "avatar": user.avatar,
            "username": user.username,
            "nickname": user.nickname,
            "roles": roles,
            "permissions": perm,
            **tokens
        }
    
    @staticmethod
    def get_routers() -> list:
        current_user = SecurityUtils.get_current_user()
        if not current_user:
            raise APIException("用户未登录或登录已过期")
        print([role.code for role in current_user.roles if not role.deleted])
        if "admin" in [role.code for role in current_user.roles if not role.deleted]:
            menu_list = SysMenu.query.filter(SysMenu.show_link==True,SysMenu.type == 0).all()
        else:
            menu_list = [menu for role in current_user.roles if not role.deleted for menu in role.menus if menu.show_link and menu.type == 0]
        if not menu_list: return []
        # 根据rank排序 并去重
        menu_list = sorted(list(set(menu_list)), key=lambda x: x.rank)
        # 构建树形路由
        menu_dict = {}
        root_menus = []
        # 转换为字典
        for menu in menu_list:
            menu_dict[menu.id] = {k: v for k, v in menu.__dict__.items() if k != '_sa_instance_state'}
            menu_dict[menu.id]["children"] = []
        # 递归构建菜单树，返回当前层级的菜单列表
        def build_tree(parent_id: int) -> list:
            children = []
            # 查找所有直接子节点
            for menu_id, menu in menu_dict.items():
                if menu["parent_id"] == parent_id:
                    # 递归构建子节点的子树
                    child_node = {
                        **menu,
                        "children": build_tree(menu_id)
                    }
                    children.append(child_node)
            # 按rank排序当前层级的节点
            return sorted(children, key=lambda x: x["rank"])
        
        # 从根节点(parent_id=0)开始构建
        root_menus = build_tree(0)
                    
        # 递归转换为前端路由格式
        # 递归转换为前端路由格式
        def convert_to_route(menu_node: dict) -> dict:
            # 基础结构
            route_node = {
                "path": menu_node["path"],
                "meta": {
                    "title": menu_node["title"]
                }
            }
            
            # 添加icon字段（如果存在）
            if menu_node.get("icon"):
                route_node["meta"]["icon"] = menu_node["icon"]
            
            # 添加rank字段（如果存在）
            if menu_node.get("rank") and menu_node["parent_id"] == 0:
                route_node["meta"]["rank"] = menu_node["rank"]
            
            # 添加name字段（如果存在）
            if menu_node.get("name"):
                route_node["name"] = menu_node["name"]
            
            # 添加component字段（如果存在且不为空）
            if menu_node.get("component") and menu_node["component"]:
                route_node["component"] = menu_node["component"]
                        
            # 添加可选meta字段
            if menu_node.get("keep_alive") is not None:
                route_node["meta"]["keepAlive"] = menu_node["keep_alive"]
            if menu_node.get("frame_src"):
                route_node["meta"]["frameSrc"] = menu_node["frame_src"]
            if menu_node.get("show_parent") is not None:
                route_node["meta"]["showParent"] = menu_node["show_parent"]
            
            # 递归处理子节点
            if menu_node.get("children") and menu_node["children"]:
                # 按rank排序子节点
                sorted_children = sorted(menu_node["children"], key=lambda x: x.get("rank", 0))
                route_node["children"] = [
                    convert_to_route(child) 
                    for child in sorted_children
                ]
            
            return route_node
        
        # 转换所有根节点
        return [convert_to_route(menu) for menu in root_menus]
    
    @staticmethod
    def refresh_token(refresh_token: str) -> dict:
        return SecurityUtils.refresh_token(refresh_token)
    
    @staticmethod
    def wx_login(code: str,state: str) -> dict:
        if not code or code == "":
            # 检查state是否存在并且已完成登陆验证
            if state in wx_uuid:
                return wx_uuid[state]
            else:
                return None
        else:   
            status,data = SecurityUtils.wx_login(code)
            if status:
                # 默认密码
                password = SecurityUtils.hash_password("wx"+data.get("username"))
                user = SysUser.get_by_username(data.get("username"))
                if not user:
                    # 新增用户并给普通权限
                    user = SysUser(
                        username=data.get("username"),
                        nickname=data.get("nickname"),
                        sex=data.get("sex"),
                        avatar=data.get("avatar"),
                        password=password,
                        status=1,
                        remark="微信用户"
                    )
                    user.save()
                    # 新增角色权限
                    user_role = SysUserRole(user_id=user.id,role_id=2)
                    user_role.save()
                    user_dept = SysUserDept(user_id=user.id,dept_id=1)
                    user_dept.save()
                wx_uuid[state] = Services.login(user.username,"wx"+user.username)
                # 获取请求IP
                ip = request.headers.get('X-Real-IP') or request.remote_addr
                # 获取UA信息
                ua = request.headers.get('User-Agent','')
                SysLoginLog.create(user.username,ip,ua,1,"微信登陆")
                # 创建
                name = data.get("nickname","微信用户")
                return '<!DOCTYPE html><html><head><title>登录成功</title><style>body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background-color:#fff;font-family:Arial,sans-serif}.success-container{text-align:center}.checkmark{width:100px;height:100px;background-color:#2ecc71;border-radius:50%;display:flex;justify-content:center;align-items:center;margin:0 auto 20px}.checkmark::before{content:"✓";color:white;font-size:60px;font-weight:bold}.message{font-size:24px;color:#34495e;font-weight:500}</style></head><body><div class="success-container"><div class="checkmark"></div><div class="message">登录成功</div><div class="message">用户名:'+name+'</div></div></body></html>'
            else:
                return '<!DOCTYPE html><html><head><title>登录失败</title><style>body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background-color:#fff;font-family:Arial,sans-serif}.error-container{text-align:center}.cross{width:100px;height:100px;background-color:#e74c3c;border-radius:50%;display:flex;justify-content:center;align-items:center;margin:0 auto 20px}.cross::before{content:"✕";color:white;font-size:60px;font-weight:bold}.message{font-size:24px;color:#34495e;font-weight:500}</style></head><body><div class="error-container"><div class="cross"></div><div class="message">登录失败</div></div></body></html>'