# Scaffold Agent 使用文档

`scaffold_agent` 是一个基于 Claude API 的智能项目脚手架 Agent，可根据自然语言需求自动创建项目结构和基础代码。

## 1. 功能概览

- 支持通过工具调用完成项目初始化流程
- 支持目录检查、文件读写、命令执行、文件匹配
- 支持交互式澄清需求（`ask_user`）
- 支持环境变量或配置文件加载 API 参数

## 2. 目录说明

```text
scaffold_agent/
├── __init__.py
├── __main__.py
├── agent.py
├── cli.py
├── config.py
├── prompts.py
├── templates/
│   ├── __init__.py
│   └── catalog.py
└── scaffold_agent_design.md
```

## 3. 环境准备

在项目根目录安装依赖：

```bash
pip install -r requirements.txt
```

设置环境变量（可放在 `.env`）：

```bash
ANTHROPIC_API_KEY=your_api_key
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-sonnet-4-20250514
```

## 4. 运行方式

### 4.1 直接传入需求

```bash
python -m scaffold_agent "创建一个带用户认证的 FastAPI 项目"
```

### 4.2 交互输入需求

```bash
python -m scaffold_agent
```

### 4.3 指定工作目录和最大循环次数

```bash
python -m scaffold_agent "创建一个 Vue 3 管理后台项目" --workspace ./demo --max-loops 30
```

### 4.4 使用配置文件

支持 `.json` / `.yaml` / `.yml`，示例：

```json
{
  "api": {
    "key": "sk-ant-xxx",
    "base_url": "https://api.anthropic.com",
    "model": "claude-sonnet-4-20250514"
  },
  "settings": {
    "max_tokens": 4096,
    "temperature": 0.2
  }
}
```

运行：

```bash
python -m scaffold_agent "创建一个 Express API 项目" --config ./config.json
```

### 4.5 日志输出（替代 print）

- 默认日志文件：`<workspace>/scaffold_agent.log`
- 可自定义日志文件路径：`--log-file`

```bash
python -m scaffold_agent "创建一个 FastAPI 项目" --workspace ./demo
python -m scaffold_agent "创建一个 FastAPI 项目" --log-file ./logs/agent.log
```

## 5. 内置工具

- `bash`：执行 shell 命令
- `write_file`：创建或覆盖文件
- `read_file`：读取文件
- `list_directory`：列目录
- `ask_user`：向用户提问
- `glob`：按模式匹配文件

> 安全限制：工具执行限制在 `workspace` 内，越界路径会被拒绝。

## 6. 运行测试

测试文件位于 `tests/scaffold_agent/`，使用 `unittest`：

```bash
python -m unittest discover -s tests/scaffold_agent -p "test_*.py"
```

当前测试覆盖：

- API 配置加载（环境变量 / JSON 配置）
- Prompt 组装与模板注入
- Tool 执行核心行为（读写、列目录、glob、ask_user、bash、路径越界）
- Agent 辅助方法（内容块规范化、文本聚合）
- Agent 运行流程（mock Claude 响应，覆盖 tool_use 循环与收敛）

## 7. 常见问题

- 报错 `ANTHROPIC_API_KEY 环境变量未设置`：请先配置 API Key
- 报错 `读取 YAML 配置需要安装 PyYAML`：安装 `PyYAML` 或使用 JSON 配置
- 结果不完整：可增大 `--max-loops` 或把需求描述更具体
