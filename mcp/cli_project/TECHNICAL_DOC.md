# MCP CLI 聊天机器人 — 技术文档

## 1. 项目概述

本项目是一个基于命令行的聊天机器人，用于演示 MCP（Model Context Protocol，模型上下文协议）客户端与服务器的协同工作方式。用户通过 CLI 与 Claude 交互，可以查询和编辑内存中的文档集合。

项目同时实现了 MCP 客户端和 MCP 服务器（实际开发中通常只需实现一端），纯粹出于教学目的。

---

## 2. 目录结构

```
cli_project/
├── .env                 # 环境变量（API 密钥、模型配置）
├── .gitignore
├── pyproject.toml       # 项目元数据与依赖声明（PEP 621）
├── uv.lock              # 依赖版本锁定文件
├── main.py              # 应用程序入口
├── mcp_client.py        # MCP 客户端 — 通过 stdio 连接 MCP 服务器
├── mcp_server.py        # MCP 服务器 — 暴露文档工具/资源/提示词
└── core/
    ├── __init__.py
    ├── chat.py           # 基础 Chat 类（智能体工具使用循环）
    ├── claude.py         # Anthropic API 封装
    ├── cli.py            # 终端 UI（prompt_toolkit：自动补全、快捷键）
    ├── cli_chat.py       # CLI 专属 Chat 子类（命令、资源、提示词处理）
    └── tools.py          # 工具发现与执行管理器
```

---

## 3. 依赖说明

| 依赖包 | 版本要求 | 用途 |
|--------|---------|------|
| `anthropic` | >=0.51.0 | Anthropic 官方 Python SDK，调用 Claude API |
| `mcp[cli]` | >=1.8.0 | MCP SDK，含客户端/服务器库及 CLI 工具 |
| `prompt-toolkit` | >=3.0.51 | 终端 UI：自动补全、按键绑定、命令历史 |
| `python-dotenv` | >=1.1.0 | 从 `.env` 文件加载环境变量 |

运行环境要求 Python >= 3.10。推荐使用 `uv` 作为包管理器。

---

## 4. 架构设计

### 4.1 整体架构图

```
                      ┌───────────┐
                      │  main.py  │  入口
                      └─────┬─────┘
                            │
            加载 .env，创建 Claude 服务，
            启动 MCP 客户端，组装各组件
                            │
                ┌───────────┴───────────┐
                │                       │
       ┌────────▼────────┐     ┌────────▼────────┐
       │   MCPClient     │     │   MCPClient     │  (通过命令行参数
       │  (doc_client)   │     │  (额外服务器)    │   传入的其他服务器)
       └────────┬────────┘     └────────┬────────┘
                │                       │
        stdio 传输                stdio 传输
       (子进程管道)              (子进程管道)
                │                       │
       ┌────────▼────────┐     ┌────────▼────────┐
       │  mcp_server.py  │     │  其他 MCP 服务器  │
       │ (DocumentMCP)   │     │                  │
       └─────────────────┘     └──────────────────┘

       ┌─────────────────┐
       │    CliApp        │  终端 UI（prompt_toolkit）
       └────────┬────────┘
                │
       ┌────────▼────────┐
       │    CliChat       │  扩展 Chat，支持 @资源 和 /命令
       └────────┬────────┘
                │
       ┌────────▼────────┐
       │   Chat (基类)    │  智能体工具使用循环
       └────────┬────────┘
                │
       ┌────────▼────────┐
       │    Claude        │  Anthropic API 封装
       └────────┬────────┘
                │
       ┌────────▼────────┐
       │  ToolManager     │  多客户端工具发现与执行
       └─────────────────┘
```

### 4.2 核心设计原则

- **多服务器支持**：`main.py` 始终启动内置文档服务器，同时支持通过命令行参数传入额外的 MCP 服务器脚本
- **工具路由**：`ToolManager` 聚合所有 MCP 客户端的工具，当 Claude 请求某个工具时，自动定位拥有该工具的客户端进行调用
- **关注点分离**：MCP 客户端处理协议通信，`Chat` 处理对话循环，`CliChat` 处理 CLI 交互逻辑，`CliApp` 处理终端 UI

---

## 5. 各模块详解

### 5.1 `mcp_server.py` — MCP 服务器

使用 `FastMCP` 创建名为 `DocumentMCP` 的服务器，内存中维护 6 个模拟文档：

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "deposition.md": "This deposition covers the testimony of ...",
    "report.pdf":    "The report details the state of ...",
    "financials.docx": "These financials outline ...",
    "outlook.pdf":   "This document presents ...",
    "plan.md":       "The plan outlines the steps ...",
    "spec.txt":      "These specifications define ..."
}
```

服务器通过 `mcp.run(transport="stdio")` 以标准输入/输出方式运行，作为客户端的子进程。

需要实现的六个 MCP 功能：

| 类型 | 功能 | 装饰器 |
|------|------|--------|
| 工具 | 读取文档内容 | `@mcp.tool()` |
| 工具 | 编辑文档（查找替换） | `@mcp.tool()` |
| 资源 | 返回所有文档 ID 列表 | `@mcp.resource()` |
| 资源 | 返回指定文档的内容 | `@mcp.resource()` |
| 提示词 | 将文档重写为 Markdown 格式 | `@mcp.prompt()` |
| 提示词 | 总结文档内容 | `@mcp.prompt()` |

### 5.2 `mcp_client.py` — MCP 客户端

封装 MCP SDK 的 `ClientSession`，提供异步上下文管理器接口。

**连接流程**（`connect` 方法，已实现）：

```
构造 StdioServerParameters
    → 通过 stdio_client 打开传输通道
    → 创建 ClientSession
    → 调用 session.initialize()
```

需要实现的五个协议方法：

| 方法 | 功能 | 预期实现 |
|------|------|---------|
| `list_tools()` | 获取服务器的工具列表 | `self.session().list_tools()` |
| `call_tool(name, input)` | 调用指定工具 | `self.session().call_tool(name, input)` |
| `list_prompts()` | 获取提示词列表 | `self.session().list_prompts()` |
| `get_prompt(name, args)` | 获取指定提示词 | `self.session().get_prompt(name, args)` |
| `read_resource(uri)` | 读取资源并解析 | `self.session().read_resource(uri)` + 按 MIME 类型解析 |

### 5.3 `core/claude.py` — Anthropic API 封装

`Claude` 类封装了 Anthropic SDK 的消息创建接口：

- 自动从环境变量读取 `ANTHROPIC_API_KEY`
- `chat()` 方法支持：工具定义、系统提示词、停止序列、扩展思考（thinking）
- `max_tokens` 固定为 8000
- 辅助方法处理消息格式转换（`Message` 对象 ↔ `MessageParam` 字典）

### 5.4 `core/chat.py` — 智能体循环（基类）

实现经典的**智能体工具使用循环**：

```
用户输入 → 预处理 → 发送给 Claude（附带工具）
    → Claude 回复 tool_use？
        是 → 执行工具 → 将结果作为用户消息追加 → 继续循环
        否 → 返回文本回复，循环结束
```

关键点：
- `_process_query()` 是钩子方法，供子类覆盖以实现输入预处理
- `self.messages` 在整个会话期间持久保存，支持多轮对话

### 5.5 `core/cli_chat.py` — CLI 交互层

继承 `Chat`，新增两大交互机制：

**@资源引用**：用户输入中的 `@doc_id` 被识别后：
1. 调用 `read_resource("docs://documents")` 获取文档 ID 列表
2. 调用 `read_resource("docs://documents/{doc_id}")` 获取文档内容
3. 内容被包裹在 `<document>` XML 标签中，作为上下文注入提示词

**/ 斜杠命令**：用户输入 `/command doc_id` 时：
1. 解析命令名和参数
2. 调用 `get_prompt(command, {"doc_id": doc_id})` 从 MCP 服务器获取提示词模板
3. 将 `PromptMessage` 转换为 Anthropic `MessageParam` 格式注入对话

辅助函数 `convert_prompt_message_to_message_param()` 负责 MCP 提示词格式到 Anthropic 消息格式的转换。

### 5.6 `core/tools.py` — 工具管理器

`ToolManager` 是一个静态工具类，负责：

- **工具聚合**：遍历所有 MCP 客户端，收集工具定义，转换为 Anthropic 工具格式（`inputSchema` → `input_schema`）
- **工具路由**：当 Claude 请求某个工具时，搜索所有客户端找到拥有该工具的那个
- **执行与错误处理**：调用工具、提取 `TextContent` 结果、构建 Anthropic 格式的 `ToolResultBlockParam`

### 5.7 `core/cli.py` — 终端 UI

基于 `prompt_toolkit` 构建，包含三个类：

| 类 | 功能 |
|----|------|
| `CommandAutoSuggest` | 灰色幽灵文本自动建议命令参数 |
| `UnifiedCompleter` | Tab 补全：`@` 触发文档 ID 补全，`/` 触发命令补全 |
| `CliApp` | 主 CLI 应用：初始化、REPL 循环、按键绑定、样式设置 |

### 5.8 `main.py` — 入口

```python
async def main():
    claude_service = Claude(model=claude_model)
    # 1. 始终启动内置文档 MCP 服务器
    # 2. 可选启动命令行参数指定的额外 MCP 服务器
    # 3. 使用 AsyncExitStack 管理所有客户端的生命周期
    # 4. 创建 CliChat + CliApp，运行 REPL
```

支持 `USE_UV` 环境变量控制启动方式（`uv run` 或 `python`）。Windows 上自动设置 `ProactorEventLoopPolicy`。

---

## 6. 数据流

### 6.1 普通查询（含 @资源引用）

```
用户输入: "请介绍 @report.pdf 的内容"
    │
    ▼
CliChat._process_query()
    ├── 识别 @report.pdf
    ├── MCPClient.read_resource("docs://documents")     → 获取文档 ID 列表
    ├── MCPClient.read_resource("docs://documents/report.pdf") → 获取文档内容
    ├── 构建结构化提示词:
    │     <query>请介绍 report.pdf 的内容</query>
    │     <context>
    │       <document name="report.pdf">文档内容...</document>
    │     </context>
    └── 追加为用户消息
    │
    ▼
Chat.run() — 智能体循环
    ├── ToolManager.get_all_tools() → 聚合所有客户端的工具
    ├── Claude.chat(messages, tools) → 调用 Anthropic API
    ├── 如果 stop_reason == "tool_use":
    │     ├── ToolManager.execute_tool_requests() → 路由并执行工具
    │     └── 将工具结果追加为用户消息 → 继续循环
    └── 如果是文本回复 → 返回给 CliApp 显示
```

### 6.2 斜杠命令

```
用户输入: "/format deposition.md"
    │
    ▼
CliChat._process_command()
    ├── 解析: command="format", doc_id="deposition.md"
    ├── MCPClient.get_prompt("format", {"doc_id": "deposition.md"})
    │     → MCP 服务器返回 PromptMessage 列表
    ├── 转换为 Anthropic MessageParam 格式
    └── 注入 self.messages
    │
    ▼
Chat.run() — 正常进入智能体循环处理
```

---

## 7. MCP 协议交互

客户端与服务器之间通过 stdio 管道交换以下 MCP 消息：

| 请求 | 响应 | 用途 |
|------|------|------|
| `ListToolsRequest` | `ListToolsResult` | 获取可用工具列表 |
| `CallToolRequest` | `CallToolResult` | 执行指定工具 |
| `ListResourcesRequest` | `ListResourcesResult` | 获取可用资源列表 |
| `ReadResourceRequest` | `ReadResourceResult` | 读取指定资源 |
| `ListPromptsRequest` | `ListPromptsResult` | 获取可用提示词列表 |
| `GetPromptRequest` | `GetPromptResult` | 获取指定提示词 |

资源 URI 方案：
- `docs://documents` — 列出所有文档 ID（直接资源）
- `docs://documents/{doc_id}` — 获取指定文档内容（模板资源）

---

## 8. 运行方式

### 配置

编辑 `.env` 文件：

```
CLAUDE_MODEL="claude-sonnet-4-5"
ANTHROPIC_API_KEY="your-api-key-here"
USE_UV=1
```

### 启动

```bash
# 使用 uv（推荐）
uv run main.py

# 使用标准 Python
python main.py

# 附加额外 MCP 服务器
uv run main.py other_server.py another_server.py
```

### 交互方式

| 方式 | 示例 | 说明 |
|------|------|------|
| 普通对话 | `1+1等于几？` | 直接与 Claude 对话 |
| @资源引用 | `请总结 @report.pdf` | 自动获取文档内容作为上下文 |
| /斜杠命令 | `/format deposition.md` | 调用 MCP 服务器预定义的提示词模板 |
| Tab 补全 | 输入 `@` 或 `/` 后按 Tab | 显示可选文档或命令列表 |

---

## 9. 项目状态

本项目是一个**教学脚手架**。基础设施（客户端连接、API 封装、智能体循环、CLI 界面）已完整实现，但 MCP 协议操作层面的功能以 TODO 形式留给学习者完成：

**服务器端**（`mcp_server.py`）— 6 个 TODO：2 个工具 + 2 个资源 + 2 个提示词

**客户端端**（`mcp_client.py`）— 5 个 TODO：`list_tools`、`call_tool`、`list_prompts`、`get_prompt`、`read_resource`

已完成的部分：
- MCP 客户端连接生命周期管理（连接、上下文管理器、清理）
- Anthropic API 集成（含工具使用、扩展思考支持）
- 智能体工具使用循环与多轮对话
- 多客户端工具路由
- 基于 prompt_toolkit 的终端 UI（自动补全、按键绑定、命令历史）
- MCP 提示词格式到 Anthropic 消息格式的转换
- 环境配置与多服务器支持
