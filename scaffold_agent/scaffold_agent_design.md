# 智能项目脚手架 Agent - 设计方案

## 1. 项目概述

### 1.1 目标
构建一个智能 Agent，能够根据用户的自然语言描述，自动创建完整的项目脚手架，包括目录结构、配置文件、基础代码模板等。

### 1.2 为什么用 Agent 而非 Workflow
| 因素 | 说明 |
|------|------|
| 任务不可预测 | 用户可能要求 Web 应用、CLI 工具、API 服务等各种类型 |
| 需要交互 | 需要询问用户的技术偏好和具体需求 |
| 灵活组合 | 相同的工具可以用不同方式组合来满足不同需求 |

---

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户输入                            │
│            "创建一个带用户认证的 FastAPI 项目"            │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Scaffold Agent                        │
│  ┌─────────────────────────────────────────────────┐    │
│  │              System Prompt                       │    │
│  │  - 角色定义：项目脚手架专家                       │    │
│  │  - 行为准则：先问后做，环境检查                   │    │
│  │  - 支持的项目类型和模板                          │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
│                          ▼                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │                 Tool Set                         │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │    │
│  │  │  bash    │ │  write   │ │  read    │        │    │
│  │  └──────────┘ └──────────┘ └──────────┘        │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │    │
│  │  │list_dir  │ │ ask_user │ │ glob     │        │    │
│  │  └──────────┘ └──────────┘ └──────────┘        │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                      生成的项目                          │
│  my_project/                                            │
│  ├── src/                                               │
│  ├── tests/                                             │
│  ├── requirements.txt                                   │
│  └── README.md                                          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Agent 循环流程

```
┌──────────────┐
│   用户输入    │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  Claude 思考  │────▶│  需要更多信息? │
└──────────────┘     └──────┬───────┘
       ▲                    │
       │              是    │    否
       │         ┌─────────┴─────────┐
       │         ▼                   ▼
       │  ┌──────────────┐   ┌──────────────┐
       │  │ 调用 ask_user │   │  调用工具执行  │
       │  └──────┬───────┘   └──────┬───────┘
       │         │                   │
       │         ▼                   ▼
       │  ┌──────────────┐   ┌──────────────┐
       │  │  用户回答     │   │  返回工具结果  │
       │  └──────┬───────┘   └──────┬───────┘
       │         │                   │
       └─────────┴───────────────────┘
                 │
                 ▼
          ┌──────────────┐
          │  任务完成?    │
          └──────┬───────┘
                 │
           是    │    否
      ┌─────────┴─────────┐
      ▼                   │
┌──────────────┐          │
│   输出结果    │          │
└──────────────┘          │
                          └──▶ 继续循环
```

---

## 3. Tool 设计

### 3.1 Tool 列表

| Tool 名称 | 描述 | 参数 |
|-----------|------|------|
| `bash` | 执行 shell 命令 | `command: str` |
| `write_file` | 创建或覆盖文件 | `path: str, content: str` |
| `read_file` | 读取文件内容 | `path: str` |
| `list_directory` | 列出目录内容 | `path: str` |
| `ask_user` | 向用户提问 | `question: str` |
| `glob` | 文件模式匹配 | `pattern: str` |

### 3.2 Tool Schema 定义

```python
tools = [
    {
        "name": "bash",
        "description": "执行 shell 命令。用于运行 git init、npm init、创建目录等操作。",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "要执行的 shell 命令"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "write_file",
        "description": "创建或覆盖文件。用于生成代码文件、配置文件等。",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件路径"
                },
                "content": {
                    "type": "string",
                    "description": "文件内容"
                }
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "read_file",
        "description": "读取文件内容。在修改文件前先读取了解当前状态。",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件路径"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_directory",
        "description": "列出目录中的文件和子目录。用于检查项目结构。",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "目录路径"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "ask_user",
        "description": "向用户提问以获取更多信息。用于询问技术偏好、项目细节等。",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "要问用户的问题"
                }
            },
            "required": ["question"]
        }
    }
]
```

---

## 4. System Prompt 设计

```
你是一个专业的项目脚手架 Agent，帮助用户快速创建项目。

## 你的能力
- 创建各种类型的项目：Web 应用、API 服务、CLI 工具、Python 包等
- 支持多种技术栈：Python (FastAPI, Flask, Django)、Node.js (Express, NestJS)、Go 等
- 生成完整的项目结构、配置文件、基础代码模板

## 工作流程
1. **理解需求**：如果用户需求不明确，使用 ask_user 工具询问：
   - 项目类型和主要功能
   - 技术栈偏好
   - 是否需要数据库、Docker、测试等

2. **环境检查**：在创建项目前：
   - 使用 list_directory 检查目标目录是否存在
   - 避免覆盖已有项目

3. **创建项目**：
   - 先创建目录结构
   - 再生成配置文件
   - 最后写入代码模板

4. **验证结果**：
   - 使用 list_directory 确认项目结构正确
   - 简要说明如何运行项目

## 注意事项
- 保持代码简洁，只生成必要的基础代码
- 添加适当的注释帮助用户理解
- 遵循各技术栈的最佳实践和目录规范
```

---

## 5. 支持的项目模板

### 5.1 Python 项目

| 模板 | 技术栈 | 典型结构 |
|------|--------|----------|
| FastAPI API | FastAPI + Uvicorn | `app/`, `models/`, `routers/` |
| Flask Web | Flask + Jinja2 | `templates/`, `static/`, `app/` |
| CLI Tool | Click / Typer | `cli/`, `commands/` |
| Python Package | setuptools | `src/`, `tests/`, `pyproject.toml` |

### 5.2 Node.js 项目

| 模板 | 技术栈 | 典型结构 |
|------|--------|----------|
| Express API | Express.js | `routes/`, `controllers/`, `models/` |
| React App | React + Vite | `src/components/`, `src/pages/` |
| Vue 2 App | Vue 2 + Vue CLI / Webpack | `src/components/`, `src/views/`, `src/router/` |
| Vue 3 App | Vue 3 + Vite | `src/components/`, `src/views/`, `src/composables/` |
| Vue 3 + TS | Vue 3 + Vite + TypeScript | `src/components/`, `src/views/`, `src/types/` |

### 5.3 Vue 项目详细配置

#### Vue 2 项目特性
| 特性 | 说明 |
|------|------|
| 状态管理 | Vuex 3.x |
| 路由 | Vue Router 3.x |
| UI 框架 | Element UI / Vuetify 2 |
| 构建工具 | Vue CLI / Webpack |
| API 风格 | Options API |

#### Vue 3 项目特性
| 特性 | 说明 |
|------|------|
| 状态管理 | Pinia (推荐) / Vuex 4.x |
| 路由 | Vue Router 4.x |
| UI 框架 | Element Plus / Vuetify 3 / Naive UI |
| 构建工具 | Vite (推荐) / Vue CLI |
| API 风格 | Composition API + `<script setup>` |

#### Vue 项目典型结构
```
vue-project/
├── public/
│   └── index.html
├── src/
│   ├── assets/              # 静态资源
│   ├── components/          # 公共组件
│   │   └── HelloWorld.vue
│   ├── views/               # 页面组件
│   │   ├── HomeView.vue
│   │   └── AboutView.vue
│   ├── router/              # 路由配置
│   │   └── index.js
│   ├── store/               # 状态管理 (Vuex/Pinia)
│   │   └── index.js
│   ├── composables/         # 组合式函数 (Vue 3)
│   ├── utils/               # 工具函数
│   ├── api/                 # API 请求
│   ├── App.vue
│   └── main.js
├── package.json
├── vite.config.js           # Vite 配置 (Vue 3)
└── vue.config.js            # Vue CLI 配置 (Vue 2)

---

## 6. 实现计划

### Phase 1: 基础框架 (核心功能)
- [ ] 创建项目目录结构
- [ ] 实现 Tool 处理函数
- [ ] 实现 Agent 循环逻辑
- [ ] 编写 System Prompt

### Phase 2: 模板系统
- [ ] FastAPI 项目模板
- [ ] Flask 项目模板
- [ ] Python CLI 工具模板
- [ ] Express.js 项目模板
- [ ] Vue 2 项目模板 (Options API + Vuex + Vue Router)
- [ ] Vue 3 项目模板 (Composition API + Pinia + Vue Router)
- [ ] Vue 3 + TypeScript 项目模板

### Phase 3: 增强功能
- [ ] 添加 Git 初始化
- [ ] Docker 配置生成
- [ ] 测试框架集成
- [ ] README 自动生成

### Phase 4: 优化完善
- [ ] 错误处理和恢复
- [ ] 用户体验优化
- [ ] 更多模板支持

---

## 7. 文件结构

```
agents_and_workflows/
├── scaffold_agent/
│   ├── __init__.py
│   ├── agent.py          # Agent 主逻辑
│   ├── tools.py          # Tool 定义和处理
│   ├── prompts.py        # System Prompt
│   └── templates/        # 项目模板
│       ├── fastapi/
│       ├── flask/
│       ├── express/
│       ├── vue2/
│       └── vue3/
├── scaffold_agent_design.md  # 本设计文档
└── agents_and_workflows_zh.md
```

---

## 8. 示例交互

### 示例 1: 创建 FastAPI 项目

```
用户: 帮我创建一个 FastAPI 项目，需要用户注册登录功能

Agent: 好的，我来帮你创建。请问几个问题：
       1. 项目名称是什么？
       2. 数据库用 SQLite 还是 PostgreSQL？
       3. 需要 Docker 配置吗？

用户: 项目叫 user-api，用 SQLite，不需要 Docker

Agent: 收到，开始创建项目...

[执行] mkdir -p user-api/app/routers user-api/app/models
[写入] user-api/app/main.py
[写入] user-api/app/models/user.py
[写入] user-api/app/routers/auth.py
[写入] user-api/requirements.txt
[执行] cd user-api && git init

Agent: 项目创建完成！结构如下：
       user-api/
       ├── app/
       │   ├── main.py
       │   ├── models/
       │   │   └── user.py
       │   └── routers/
       │       └── auth.py
       └── requirements.txt

       运行方式：
       cd user-api
       pip install -r requirements.txt
       uvicorn app.main:app --reload
```

### 示例 2: 创建 Vue 3 项目

```
用户: 创建一个 Vue 3 管理后台项目

Agent: 好的，我来帮你创建 Vue 3 项目。请问几个问题：
       1. 项目名称是什么？
       2. 需要 TypeScript 支持吗？
       3. 状态管理用 Pinia 还是 Vuex？
       4. UI 框架选择？(Element Plus / Naive UI / 不需要)

用户: 项目叫 admin-dashboard，要 TypeScript，用 Pinia，Element Plus

Agent: 收到，开始创建项目...

[执行] mkdir -p admin-dashboard/src/{components,views,router,store,api,utils,types}
[写入] admin-dashboard/package.json
[写入] admin-dashboard/vite.config.ts
[写入] admin-dashboard/tsconfig.json
[写入] admin-dashboard/src/main.ts
[写入] admin-dashboard/src/App.vue
[写入] admin-dashboard/src/router/index.ts
[写入] admin-dashboard/src/store/index.ts
[写入] admin-dashboard/src/views/HomeView.vue
[执行] cd admin-dashboard && git init

Agent: 项目创建完成！结构如下：
       admin-dashboard/
       ├── src/
       │   ├── components/
       │   ├── views/
       │   │   └── HomeView.vue
       │   ├── router/
       │   │   └── index.ts
       │   ├── store/
       │   │   └── index.ts
       │   ├── api/
       │   ├── utils/
       │   ├── types/
       │   ├── App.vue
       │   └── main.ts
       ├── package.json
       ├── vite.config.ts
       └── tsconfig.json

       运行方式：
       cd admin-dashboard
       npm install
       npm run dev
```

### 示例 3: 创建 Vue 2 项目

```
用户: 我需要一个 Vue 2 项目，要兼容 IE11

Agent: 好的，Vue 2 + Vue CLI 可以支持 IE11。请问：
       1. 项目名称是什么？
       2. 需要 Vuex 状态管理吗？
       3. UI 框架选择？(Element UI / Vuetify 2 / 不需要)

用户: 叫 legacy-app，需要 Vuex，用 Element UI

Agent: 收到，开始创建项目...

[执行] mkdir -p legacy-app/src/{components,views,router,store,api,utils}
[写入] legacy-app/package.json
[写入] legacy-app/vue.config.js
[写入] legacy-app/babel.config.js
[写入] legacy-app/src/main.js
[写入] legacy-app/src/App.vue
[写入] legacy-app/src/router/index.js
[写入] legacy-app/src/store/index.js
[执行] cd legacy-app && git init

Agent: 项目创建完成！

       运行方式：
       cd legacy-app
       npm install
       npm run serve
```

---

## 9. 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| LLM | Claude API | 强大的代码生成和推理能力 |
| 语言 | Python | 与学习材料一致，生态丰富 |
| 命令执行 | subprocess | 标准库，安全可控 |

---

## 10. 配置管理

### 10.1 支持自定义 API 配置

Agent 支持通过环境变量或配置文件自定义 Claude API 设置：

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| API Key | `ANTHROPIC_API_KEY` | - | Claude API 密钥 (必填) |
| Base URL | `ANTHROPIC_BASE_URL` | `https://api.anthropic.com` | API 端点地址 |
| Model | `ANTHROPIC_MODEL` | `claude-sonnet-4-20250514` | 使用的模型 |

### 10.2 配置文件示例

**方式 1: 环境变量 (.env)**
```bash
# .env
ANTHROPIC_API_KEY=sk-ant-xxxxx
ANTHROPIC_BASE_URL=https://api.anthropic.com  # 可选，支持代理/自定义端点
ANTHROPIC_MODEL=claude-sonnet-4-20250514              # 可选，指定模型
```

**方式 2: 配置文件 (config.yaml)**
```yaml
# config.yaml
api:
  key: sk-ant-xxxxx          # 或从环境变量读取
  base_url: https://api.anthropic.com
  model: claude-sonnet-4-20250514

# 可选配置
settings:
  max_tokens: 4096
  temperature: 0.7
```

### 10.3 代码实现

```python
import os
from dataclasses import dataclass
from typing import Optional
import anthropic

@dataclass
class APIConfig:
    """Claude API 配置"""
    api_key: str
    base_url: str = "https://api.anthropic.com"
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096

    @classmethod
    def from_env(cls) -> "APIConfig":
        """从环境变量加载配置"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY 环境变量未设置")

        return cls(
            api_key=api_key,
            base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        )

    @classmethod
    def from_file(cls, path: str) -> "APIConfig":
        """从配置文件加载"""
        import yaml
        with open(path) as f:
            config = yaml.safe_load(f)

        api_config = config.get("api", {})
        return cls(
            api_key=api_config.get("key") or os.getenv("ANTHROPIC_API_KEY"),
            base_url=api_config.get("base_url", "https://api.anthropic.com"),
            model=api_config.get("model", "claude-sonnet-4-20250514")
        )

def create_client(config: Optional[APIConfig] = None) -> anthropic.Anthropic:
    """创建 Claude 客户端"""
    if config is None:
        config = APIConfig.from_env()

    return anthropic.Anthropic(
        api_key=config.api_key,
        base_url=config.base_url
    )
```

### 10.4 支持的模型

| 模型 | Model ID | 适用场景 |
|------|----------|----------|
| Claude Sonnet 4 | `claude-sonnet-4-20250514` | 平衡性能和成本 (推荐) |
| Claude Opus 4 | `claude-opus-4-20250514` | 复杂任务，最强能力 |
| Claude Haiku | `claude-haiku-3-5-20241022` | 快速响应，低成本 |

### 10.5 使用第三方代理

如果需要使用代理服务（如 Azure OpenAI 兼容接口或其他代理），只需修改 `base_url`：

```bash
# 使用代理服务
ANTHROPIC_BASE_URL=https://your-proxy.example.com/v1
```

---

## 11. 下一步

1. 开始实现 Phase 1 基础框架
2. 先完成核心 Agent 循环
3. 实现基础 Tool
4. 测试简单的项目创建流程
