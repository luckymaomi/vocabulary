# 连词成句

把高频词放回句子里学。

`连词成句` 是一个英语词汇学习工具：用情境句承载词汇，用词库做检索和复习，用释义页快速确认含义。它适合把零散单词变成可阅读、可理解、可反复回看的材料。

## 它能做什么

- 📚 查看 COCA 高频词库批次
- 🔎 查询单词释义和音标
- 🧩 阅读情境句，点击词汇跳转释义
- 🖼️ 展示每日短句图片
- 🤖 使用智能体做翻译、解释和自定义任务

## 项目结构

```text
main.py              FastAPI 入口
core/                配置、数据库、日志、加载状态和访问记录
routers/             API 路由
services/            可复用业务服务
templates/           页面模板
static/              CSS、JS 和图片资源
data_vocabulary/     词库文本
data_sentence/       情境句文本
TodayPhrase/         今日短句图片
tests/               pytest 测试
```

## 启动

```powershell
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 5000
```

访问：`http://127.0.0.1:5000`

## 验证

```powershell
npm.cmd run verify
```

## License

MIT
