---
name: vocabulary-development
description: 维护连词成句项目时使用。适用于修改 FastAPI 应用、路由、服务、数据库加载、词库、句库、静态前端、AI 能力、README、spec、AGENTS.md、测试或运行配置；要求先 research，再 plan，再按生产级验收闭环交付。
---

# Vocabulary Development

每次接手都当作新项目。

先看事实，再做判断，最后行动。

事实来自当前 `spec.md`、`AGENTS.md`、`plan.md`、`README.md`、`.codex/skills/`、`main.py`、`core/`、`routers/`、`services/`、`templates/`、`static/`、`tests/`、配置文件、git 状态、命令结果和 owner 明确输入。

## 铁律

- 先 research，再计划，再实现。
- 没有完成主链路调查，不动局部代码。
- 禁止兼容转发、旧别名导出、旧语义包装和历史命名适配层。
- 禁止把未实现能力写成当前产品事实。
- 禁止用根目录 `.cmd` 作为开发主入口；统一入口看根 `package.json`。
- 不交半成品。架构、类型、测试、文档和验证必须在同一交付闭环内完成。

## 当前产品主干

当前产品是英语词汇学习工具：

- 词库批次浏览。
- 单词释义查询。
- 情境句阅读。
- 今日短句展示。
- AI 普通对话和流式对话。

## 技术边界

- 根目录是 FastAPI 应用目录。
- `main.py` 是入口。
- `core/` 管配置、数据库、连接池、日志和运行状态。
- `routers/` 管 HTTP 路由。
- `services/` 管可复用业务服务。
- `templates/` 和 `static/` 管页面。
- `tests/unit/` 管 pytest 测试。

## 文件职责审查

单一职责看变化原因，不看行数。

超过 300 行必须触发职责审查，但不是自动拆分理由。

职责混杂时按变化原因拆分：路由、服务、数据访问、文件扫描、运行配置、测试工具和文档事实必须有清晰边界。

## 验证

完整验证命令：

```text
npm.cmd run verify
```

涉及 Python 逻辑时至少覆盖：

```text
python -m pytest tests/unit
python -c "import main; print('app import ok')"
```

## 交付标准

接到明确问题后，把 research、设计、实现、测试、文档同步和验证收成一个完整交付。

不交半成品。

把“顶尖标准”翻成可验收的终局，不写成“继续优化”。

把任务定成生产级封顶验收，不写成后续优化或逐步改进。

不能一次闭环时，说明客观阻塞、已完成事实和剩余风险。

大改完成前运行项目完整验证命令。当前项目的完整验证命令必须在 `package.json` 中定义为：

```powershell
npm.cmd run verify
```

commit / push 只在项目所有者明确要求时执行。

## Caveman

短。准。硬。

少废话，不少判断。
少解释，不少证据。
少抽象，不少边界。
说不清，先别改。
