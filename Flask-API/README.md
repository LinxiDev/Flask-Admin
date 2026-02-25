# 使用 uv 完成项目初始化
```bash
# 初始化
uv init Flask-API
cd Flask-API
# 创建虚拟环境
uv venv
# Win.bat 激活虚拟环境
& E:/Download/软件开发/Flask/Flask-API/.venv/Scripts/Activate.bat
# 安装依赖
uv sync
# 查看项目依赖数
uv tree
# 运行项目
uv run main.py
# 更新依赖
uv lock --upgrade-package pydantic
```

## Git 提交规范
| 类型(Type) | 描述(Description) | 示例(Example) |
|------------|------------------|---------------|
| feat | 新增/修改功能 | `feat: 新增用户登录功能` |
| fix | 修复 bug | `fix: 修复登录页面密码验证错误` |
| docs | 文档相关 | `docs: 更新API文档说明` |
| style | 代码格式调整(不影响运行) | `style: 调整代码缩进和空格格式` |
| refactor | 代码重构 | `refactor: 优化用户服务模块结构` |
| perf | 性能优化 | `perf: 提升数据库查询效率` |
| test | 增加测试 | `test: 添加用户模块单元测试` |
| chore | 构建工具或辅助工具变动 | `chore: 更新依赖包版本` |
| revert | 撤销之前的提交 | `revert: revert: feat: 新增用户登录功能 (回覆版本：abc1234)` |
| version | 更新版本信息 | `version: 更新版本号至v1.2.0` |