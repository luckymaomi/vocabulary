# Contributing

## 基本流程

1. 先读 `AGENTS.md`、`spec.md` 和当前 `plan.md`。
2. 涉及代码修改时，先确认需求边界，再更新计划。
3. 按当前实现写代码，不保留历史兼容层。
4. 为核心逻辑补 pytest 测试。
5. 收尾前运行：

```powershell
npm.cmd run verify
```

## 文档规则

- 产品事实写入 `spec.md`。
- 用户入口写入 `README.md`。
- 旧资料归档到 `history.md`。
- 任务执行过程写入 `plan.md`。

## 提交规则

commit / push 只在项目所有者明确要求时执行。
