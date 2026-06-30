# Vocabulary 根目录整理和生产级验收 Plan

## 1. 需求文档

用户要求把 `vocabulary` 整理成和 `mo` 同一类的项目结构：把当前 `app/` 内的应用文件移动到仓库根目录，补齐 `AGENTS.md`、项目 skill、`spec.md`、MIT 协议、README、贡献规范、验证入口、测试和生产级验收。

业务完成标准：根目录就是可运行应用目录；文档只记录当前事实；没有旧式散落脚本和过期指南作为主入口；根目录提供统一验证命令；pytest 自动化测试通过。

## 2. 当前事实

- 当前应用是 FastAPI + Jinja 模板 + 原生静态前端。
- 现有应用文件集中在 `app/`：`main.py`、`requirements.txt`、`core/`、`routers/`、`templates/`、`static/`、词库、句库和今日短句资源。
- 根目录存在旧式文档和脚本：`开发指南.md`、`开发指南-模块化与复用.md`、`Nginx命令手册.txt`、`提交git前运行.py`。
- 当前没有统一根验证入口、项目级 skill、标准开源文档和测试目录。
- `routers/ai.py` 超过 300 行且混合路由、API key 读取和远程 AI 请求重试，需按职责拆分。
- `core/ip_tracker.py` 超过 300 行，本轮触发职责审查；若变化原因仍围绕访问记录生命周期，则不机械拆分。

## 3. 失败测试

以下任一情况视为失败：

- `app/` 仍作为主要应用目录存在。
- 根目录继续保留旧式手工脚本和散落指南作为主入口。
- 文档写未实现能力、旧状态或伪兼容。
- 没有 `npm.cmd run verify` 统一验证入口。
- 没有覆盖核心 Python 逻辑的自动化测试。
- 超过 300 行文件未触发职责审查记录。
- 验证命令失败。

## 4. 目标

- 将 `app/` 中当前应用文件移动到仓库根目录。
- 补齐 `AGENTS.md`、`spec.md`、`README.md`、`LICENSE`、`SECURITY.md`、`CONTRIBUTING.md`、`plan.example.md`、`.gitignore`、`.codex/skills/`。
- 删除旧式根目录指南、Nginx 手册和手工提交脚本。
- 新增根 `package.json`，统一定义 `npm.cmd run verify`。
- 新增 pytest 单元测试。
- 将 AI 客户端职责从路由中拆出。
- 运行完整验证并收口。

## 5. 不做范围

- 不重写 UI。
- 不迁移到 React、Vue 或前后端分离框架。
- 不删除现有词库、句库、今日短句和静态资源。
- 不改变当前核心 API 路径。
- 不执行 commit 或 push，除非 owner 明确要求。

## 6. 设计

- 根目录直接承载 FastAPI 应用：`main.py`、`core/`、`routers/`、`services/`、`templates/`、`static/`、`data_vocabulary/`、`data_sentence/`。
- `tests/unit/` 放核心纯逻辑和可隔离服务测试。
- AI 路由只处理 HTTP 参数、响应和事件记录；API key 读取、mask、payload key 选择和远程调用放到 `services/ai_client.py`。
- 根 `package.json` 只作为统一命令入口，不把 Python 项目伪装成 Node 项目。

## 7. 实施任务

- [ ] T001 安全移动 `app/` 内容到仓库根目录。
- [ ] T002 补齐根目录标准文档和项目级 skill。
- [ ] T003 删除旧式根目录指南、Nginx 手册和手工提交脚本。
- [ ] T004 新增统一验证入口和 Python 测试配置。
- [ ] T005 拆分 AI 客户端职责，保持 API 行为不变。
- [ ] T006 新增 pytest 测试覆盖工具函数、AI key 处理、数据库连接池和路由基础行为。
- [ ] T007 运行 pytest 和完整验证。
- [ ] T008 运行导入检查，确认 FastAPI 应用主入口可加载。
- [ ] T009 更新收口记录。

## 8. 验证计划

```powershell
npm.cmd run verify
```

## 9. 收口

待执行。
