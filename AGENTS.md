# Vocabulary Agent 工作规约

本文件是本仓库的最高工作约束。产品事实看 `spec.md`，当前任务执行状态看 `plan.md`。

## 基础约束

- 始终使用简体中文和 owner 交流。
- 阅读本仓库文本文件时按 UTF-8 读取；PowerShell 中文显示乱码时，不要误判文件损坏。
- PowerShell 中运行 Node/npm 命令使用 `npm.cmd`、`npx.cmd`。
- 不回滚 owner 已有改动，除非 owner 明确要求。
- 遇到脏工作区，只处理当前任务相关文件。
- commit / push 只在 owner 明确要求时执行。
- 不使用阶段性版本命名组织产品事实、计划或回复。
- 禁止跨文件机械替换、批量正则替换或大小写不受控的命名迁移。
- 禁止兼容转发、旧别名导出、旧语义包装、历史命名适配层或为了平滑过渡保留的中间文件。
- 当前代码只服务当前生效实现。

## 根文档边界

- `AGENTS.md`：agent 工作规则和仓库协作纪律。
- `spec.md`：当前产品事实、业务边界、技术边界、验收标准和开源协议。
- `plan.md`：当前任务的单文件规格驱动执行合同。
- `plan.example.md`：后续任务计划模板。
- `README.md`：面向用户和新读者的项目入口。
- `history.md`：迁移前旧文档归档，只作历史参考。
- `LICENSE`：MIT License 权威文本。
- `SECURITY.md`：安全报告、配置和运行数据处理规则。
- `CONTRIBUTING.md`：贡献流程和文档驱动规则。
- `.gitignore`：不进入版本控制的文件边界。
- `.codex/skills/vocabulary-development/SKILL.md`：本项目开发、架构、测试和交付规则。
- `.codex/skills/plan/SKILL.md`：`plan.md` 写作和执行规则。

## Skills

项目级 skill 放在 `.codex/skills/`。

修改 FastAPI、路由、服务、数据库加载、静态前端、词库、句库、AI 能力、测试、spec、README、AGENTS.md 或运行配置时，先读 `.codex/skills/vocabulary-development/SKILL.md`。

中大型开发、跨模块重构、生产级验收、恢复演练、架构硬化、评测闭环，或任何不能靠一次小补丁完成的任务，先读 `.codex/skills/plan/SKILL.md`，并维护根目录 `plan.md`。

## 文件职责

单一职责看变化原因，不看行数。

超过 300 行必须触发职责审查，但不是自动拆分理由。

职责混杂时必须按变化原因拆分：HTTP 路由、业务服务、数据访问、文件扫描、运行配置、测试工具和文档事实不能硬塞在同一文件里。

## 验证规则

- 代码任务收尾前必须运行根目录验证命令。
- 当前完整验证命令是 `npm.cmd run verify`。
- 无法运行验证时必须说明具体命令、失败原因和剩余风险。

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
