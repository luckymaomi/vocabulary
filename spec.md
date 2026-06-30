# Vocabulary Spec

`spec.md` 记录当前产品事实、业务边界、技术边界、架构约束、验收标准和开源协议。未实现能力不能写成当前能力。

## 产品定位

连词成句是英语词汇学习工具。它用情境句组织高频词，用词库支持检索和复习，用释义页帮助用户快速确认单词含义。

## 当前事实

- 根目录是 FastAPI 应用目录。
- `main.py` 是应用入口。
- `core/` 存放配置、数据库加载、连接池、日志、加载状态、访问记录。
- `routers/` 存放 HTTP API 路由。
- `services/` 存放可复用业务服务。
- `templates/` 和 `static/` 提供当前页面。
- `data.xlsx` 是启动时加载到 SQLite 的词库来源。
- `data_vocabulary/` 是词库文本数据。
- `data_sentence/` 是情境句文本数据。
- `TodayPhrase/` 是今日短句图片来源。
- 当前完整验证命令是 `npm.cmd run verify`。
- 当前自动化测试使用 pytest。

## 用户路径

### 词库

用户进入词库批次列表，选择一个批次后查看单词、音标和释义。

### 语境

用户进入情境句列表，打开文本后阅读整段内容。页面支持下载当前文本，并可把全文发送到智能体。

### 释义

用户查询单词后，后端从 SQLite 词库中查找标准化单词并返回释义。

### 智能体

用户可以提供 API key 或选择本地配置中的 key，向 SiliconFlow Chat Completions 接口发起普通或流式对话。

### 今日短句

系统从 `TodayPhrase/` 中查找图片并返回页面可展示的图片地址。

## 架构边界

- HTTP 参数校验和响应格式属于 `routers/`。
- 可复用业务逻辑属于 `services/`。
- 数据库重建、连接池和加载状态属于 `core/`。
- 静态页面交互属于 `static/js/`。
- 样式属于 `static/css/`。
- 大型词库和句库数据保留在数据目录，不写进 Python 代码。

## 数据边界

- 运行生成的 SQLite、日志、缓存和临时文件不进入版本控制。
- 本地私有配置不作为产品事实写入文档。
- `history.md` 是旧文档归档，不作为当前实现规则。

## 当前不做

- 不做账号系统。
- 不做云同步。
- 不做移动端原生应用。
- 不做前后端分离重写。
- 不做浏览器级 E2E 验收。

## 验收标准

- `npm.cmd run verify` 通过。
- pytest 测试通过。
- `main.py` 可被 Python 正常导入。
- 根目录不保留旧式手工脚本作为主入口。
- 文档、skill 和实际目录结构一致。
- 超过 300 行文件已触发职责审查。

## 开源协议

本项目代码选择 MIT License。

第三方依赖遵循各自许可证，包括 FastAPI、Uvicorn、HTTPX、OpenPyXL、Pandas、aiofiles、python-multipart、pytest 等。
