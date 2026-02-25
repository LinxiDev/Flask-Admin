# 导入 Pydantic 的 BaseModel 和 Field 用于数据模型定义
from pydantic import BaseModel, Field,field_validator
# 导入 typing 的 Optional 和 List 用于类型提示
from typing import Optional


class Query(BaseModel):
    name: Optional[str] = Field(None, description="角色名称", example="管理员")

    # 将空字符串转换为None
    @field_validator('name',mode='before')
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v
    
class Create(BaseModel):
    menuType: Optional[int] = Field(0, description="菜单类型", example=0)
    parentId: Optional[int] = Field(0, description="父级菜单id", example=0)
    title: str = Field(..., description="菜单标题", example="测试菜单")
    name: str = Field(..., description="菜单名称", example="Test")
    path: str = Field(..., description="路由路径", example="/Test")
    component: Optional[str] = Field("", description="组件路径", example="")
    rank: Optional[int] = Field(99, description="排序", example=99)
    redirect: Optional[str] = Field("", description="重定向路径", example="")
    icon: Optional[str] = Field("", description="图标", example="")
    extraIcon: Optional[str] = Field("", description="额外图标", example="")
    enterTransition: Optional[str] = Field("", description="进入过渡动画", example="")
    leaveTransition: Optional[str] = Field("", description="离开过渡动画", example="")
    activePath: Optional[str] = Field("", description="激活路径", example="")
    auths: Optional[str] = Field("", description="权限标识", example="")
    frameSrc: Optional[str] = Field("", description="内嵌框架链接", example="")
    frameLoading: Optional[bool] = Field(True, description="框架加载状态", example=True)
    keepAlive: Optional[bool] = Field(False, description="是否缓存", example=False)
    hiddenTag: Optional[bool] = Field(False, description="隐藏标签", example=False)
    fixedTag: Optional[bool] = Field(False, description="固定标签", example=False)
    showLink: Optional[bool] = Field(True, description="显示链接", example=True)
    showParent: Optional[bool] = Field(False, description="显示父级", example=False)

class Update(Create):
    id: Optional[int] = Field(...,description="菜单ID",examples=1)