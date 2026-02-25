# 导入类型定义
from typing import Union
# 导入用户模型
from app.models import SysMenu
# 导入数据库操作对象
from app.common.extension import db
# 导入统一响应
from app.common.exceptions import APIException
# 导入数据模型定义
from .schemas import Query, Create, Update


class Services:
    @staticmethod
    def list(q: Query) -> Union[dict, list]:
        if q.name:
            query = SysMenu.query.filter(SysMenu.title.ilike(f"%{q.name}%")).order_by(SysMenu.rank).all()
        else:
            query = SysMenu.query.order_by(SysMenu.rank).all()
        return [ {
            "parentId": menu.parent_id,
            "id": menu.id,
            "menuType": menu.type,
            "title": menu.title,
            "name": menu.name,
            "path": menu.path,
            "component": menu.component,
            "rank": menu.rank,
            "redirect": menu.redirect,
            "icon": menu.icon,
            "extraIcon": menu.extra_icon,
            "exterTransition": menu.enter_transition,
            "leaveTransition": menu.leave_transition,
            "activePath": menu.active_path,
            "auths": menu.auths,
            "frameSrc": menu.frame_src,
            "frameLoading": menu.frame_loading,
            "KeepAlive": menu.keep_alive,
            "hiddenTag": menu.hidden_tag,
            "fixedTag": menu.fixed_tag,
            "showLink": menu.show_link,
            "showParent": menu.show_parent,
        } for menu in query]
    

    @staticmethod
    def add(body: Create) -> dict:
        # 查询路由名称不能重复
        if SysMenu.query.filter_by(name=body.name, type=0).first() is not None:
            raise APIException(msg="菜单路由名称不能重复")
        
        # 构建菜单对象，只设置非空值
        menu_data = {
            'parent_id': body.parentId,
            'title': body.title,
            'name': body.name,
            'path': body.path,
        }

        # 只有当字段有值时才添加到数据中
        if body.component:
            menu_data['component'] = body.component
        if body.rank is not None:
            menu_data['rank'] = body.rank
        if body.redirect:
            menu_data['redirect'] = body.redirect
        if body.icon:
            menu_data['icon'] = body.icon
        if body.extraIcon:
            menu_data['extra_icon'] = body.extraIcon
        if body.enterTransition:
            menu_data['enter_transition'] = body.enterTransition
        if body.leaveTransition:
            menu_data['leave_transition'] = body.leaveTransition
        if body.activePath:
            menu_data['active_path'] = body.activePath
        if body.auths:
            menu_data['auths'] = body.auths
        if body.frameSrc:
            menu_data['frame_src'] = body.frameSrc
        if body.menuType is not None:
            menu_data['type'] = body.menuType
        
        # 处理布尔值字段
        if body.frameLoading is not None:
            menu_data['frame_loading'] = body.frameLoading
        if body.keepAlive is not None:
            menu_data['keep_alive'] = body.keepAlive
        if body.hiddenTag is not None:
            menu_data['hidden_tag'] = body.hiddenTag
        if body.fixedTag is not None:
            menu_data['fixed_tag'] = body.fixedTag
        if body.showLink is not None:
            menu_data['show_link'] = body.showLink
        if body.showParent is not None:
            menu_data['show_parent'] = body.showParent
        
        # 使用基础模型的save方法
        SysMenu(**menu_data).save()
        return None


    @staticmethod
    def delete(id: Union[int, str]) -> dict:
        # 查询菜单
        # 使用基础模型的get_by_id方法
        menu = SysMenu.get_by_id(id)
        if menu is None:
            raise APIException(msg="菜单不存在")
        # 使用基础模型的delete方法
        menu.delete()
        return None

    @staticmethod
    def edit(body: Update) -> dict:
        # 使用基础模型的get_by_id方法
        menu = SysMenu.get_by_id(body.id)
        if menu is None:
            raise APIException(msg="菜单不存在")
        
        # 检查路由名称是否与其他菜单重复（排除当前菜单）
        existing_menu = SysMenu.query.filter(
            SysMenu.name == body.name,
            SysMenu.id != body.id,
            SysMenu.type == 0,
        ).first()
        if existing_menu is not None:
            raise APIException(msg="菜单路由名称不能重复")
        
        # 构建更新数据，只更新非空值
        update_data = {}
        
        # 必填字段总是更新
        update_data['title'] = body.title
        update_data['name'] = body.name
        update_data['path'] = body.path
        
        # 只有当字段有值时才更新
        if body.component is not None:
            update_data['component'] = body.component
        if body.parentId is not None:
            update_data['parent_id'] = body.parentId
        if body.rank is not None:
            update_data['rank'] = body.rank
        if body.redirect is not None:
            update_data['redirect'] = body.redirect
        if body.icon is not None:
            update_data['icon'] = body.icon
        if body.extraIcon is not None:
            update_data['extra_icon'] = body.extraIcon
        if body.enterTransition is not None:
            update_data['enter_transition'] = body.enterTransition
        if body.leaveTransition is not None:
            update_data['leave_transition'] = body.leaveTransition
        if body.activePath is not None:
            update_data['active_path'] = body.activePath
        if body.auths is not None:
            update_data['auths'] = body.auths
        if body.frameSrc is not None:
            update_data['frame_src'] = body.frameSrc
        if body.menuType is not None:
            update_data['type'] = body.menuType
        
        # 处理布尔值字段
        if body.frameLoading is not None:
            update_data['frame_loading'] = body.frameLoading
        if body.keepAlive is not None:
            update_data['keep_alive'] = body.keepAlive
        if body.hiddenTag is not None:
            update_data['hidden_tag'] = body.hiddenTag
        if body.fixedTag is not None:
            update_data['fixed_tag'] = body.fixedTag
        if body.showLink is not None:
            update_data['show_link'] = body.showLink
        if body.showParent is not None:
            update_data['show_parent'] = body.showParent
        
        # 使用基础模型的update方法
        menu.update(**update_data)
        return None
            