Anthropic 应用 - Claude  Code 与 Computer Use

# Anthropic 应用

在本模块中，我们将探索 Anthropic 构建的两个强大应用：Claude  Code 和 Computer Use。它们不仅仅是实用的工具——它们更是 AI Agent 实际应用的完美示例。通过理解它们的工作原理，你将为后续构建自己的 Agent 打下坚实的基础。

## 我们的计划

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542875%2F10_-_001_-_Anthropic_Apps_02.1748542875572.jpg)我们将按照循序渐进的方式来构建你的理解：

* **Claude  Code** - 从这个运行在终端中的智能编码助手开始
* **Computer Use** - 探索这套让 Claude 与桌面应用交互的工具集
* **Agent** - 理解是什么让这些应用能够成功地作为 Agent 运行

## Claude  Code

Claude  Code 是一个基于终端的编码助手，可以帮助你完成各种编程任务。可以把它想象成在命令行中随时待命的 Claude，随时准备：

* 编辑文件和修复 bug
* 回答编程问题
* 协助开发工作流程

我们将完整演示设置过程，然后在一个小型示例项目上使用 Claude  Code，让你能够确切地看到它在实践中是如何运作的。

## Computer Use

Computer Use 将 Claude 的能力提升到了一个全新的层次。它是一套工具集合，允许 Claude 与完整的桌面计算机环境进行交互。这意味着 Claude 可以：

* 访问网站和浏览互联网
* 与桌面应用程序交互
* 执行需要视觉界面导航的任务

与纯文本交互相比，这极大地扩展了可能性。

## 为什么这些对 Agent 很重要

Claude  Code 和 Computer Use 都是理解 Agent 的绝佳案例研究。它们展示了使 Agent 有效运作的关键原则：

* 工具集成与使用
* 多步骤任务执行
* 环境交互
* 自主问题解决

通过研究这些实际应用案例，你将深入了解是什么让 Claude  Code 和 Computer Use 如此成功，这将为你自己的 Agent 开发工作提供启发。

让我们在下一节开始 Claude  Code 的设置过程。

# Claude  Code 设置

Claude  Code 是一个基于终端的编码助手，直接运行在你的命令行中。可以把它想象成在终端中随时待命的 Claude，随时帮助你处理任何正在进行的编码任务。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542849%2F10_-_002_-_Claude_Code_Setup_00.1748542849392.jpg)

## Claude  Code 能做什么

Claude  Code 配备了一套全面的工具来帮助你的开发工作流程：

* **文件操作** - 在项目中搜索、读取和编辑文件
* **终端访问** - 直接从对话中运行命令
* **网络访问** - 搜索文档、获取代码示例等
* **MCP 服务器支持** - 通过连接 MCP 服务器添加额外工具

MCP 集成特别强大，因为这意味着你可以通过添加数据库、API 或任何其他你使用的服务的专用工具来扩展 Claude  Code 的能力。

Claude  Code 可在 MacOS、Windows WSL 和 Linux 上运行，因此无论你的开发环境如何都可以使用它。

## 安装

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542850%2F10_-_002_-_Claude_Code_Setup_10.1748542849909.jpg)设置 Claude  Code 只需三个步骤：

1. **安装 Node.js**：从 nodejs.org/en/download 下载安装（可以在终端中运行 `npm help` 检查是否已安装）
2. **安装 Claude  Code**：使用命令：`npm install -g @anthropic-ai/claude-code`
3. **启动并登录**：在终端中运行 `claude`

当你第一次运行 `claude` 命令时，它会提示你登录 Anthropic 账户。如需更详细的说明，完整的设置指南可在 docs.anthropic.com 上获取。

设置完成后，你将在终端中直接使用 Claude，随时准备帮助你处理任何编码项目或任务。

# Claude  Code 实战

Claude  Code 不仅仅是一个编写代码的工具——它旨在伴随你完成软件项目的每一个阶段。可以把它看作团队中的另一位工程师，能够处理从初始设置到部署和支持的所有工作。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542928%2F10_-_003_-_Claude_Code_in_Action_01.1748542928114.jpg)

## /init 命令

当你开始在项目中使用 Claude  Code 时，首先要做的是运行 `/init` 命令。这会告诉 Claude 扫描整个代码库，了解项目的结构、依赖关系、编码风格和架构。

Claude 会将学到的所有内容总结在一个名为 `CLAUDE.md` 的特殊文件中。这个文件会自动作为上下文包含在所有未来的对话中，因此 Claude 能记住项目的重要细节。

你可以为不同的作用域设置多个 CLAUDE.md 文件：

* **项目级** - 在项目中所有工程师之间共享
* **本地级** - 你的个人笔记，不会提交到 git
* **用户级** - 在你的所有项目中使用

运行 `/init` 时，你可以为希望 Claude 关注的领域添加特别说明。生成的文件将包含 Claude 应该遵循的构建命令、编码规范和项目特定模式。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542928%2F10_-_003_-_Claude_Code_in_Action_05.1748542928626.jpg)你还可以使用 `#` 命令快速向 CLAUDE.md 文件添加笔记。例如，输入 `# Always use descriptive variable names` 会提示你将此规范添加到项目级、本地级或用户级记忆中。

## 常用工作流程

当你把 Claude 作为效率倍增器来使用时，它能发挥最佳效果。你提供的上下文和结构越多，得到的结果就越好。以下是最有效的工作流程：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542929%2F10_-_003_-_Claude_Code_in_Action_11.1748542928969.jpg)

### 步骤 1：向 Claude 提供上下文

在让 Claude 构建某些功能之前，先确定代码库中与你想创建的功能相关的文件。首先让 Claude 阅读和分析这些文件。这能让 Claude 了解你的编码模式和现有功能，以便在此基础上进行构建。

### 步骤 2：让 Claude 规划解决方案

不要直接跳到实现阶段，而是让 Claude 思考问题并创建计划。明确告诉 Claude 暂时不要写任何代码——只专注于方法和所需的步骤。

### 步骤 3：让 Claude 实现解决方案

一旦有了可靠的计划，就让 Claude 实现它。Claude 将根据你们已经一起完成的上下文和规划工作来编写代码。

## 测试驱动开发工作流程

为了获得更好的结果，你可以使用测试驱动的方法：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542929%2F10_-_003_-_Claude_Code_in_Action_17.1748542929416.jpg)

1. **向 Claude 提供上下文** - 与之前一样，向 Claude 展示相关文件
2. **让 Claude 思考测试用例** - 让 Claude 头脑风暴哪些测试可以验证你的新功能
3. **让 Claude 实现这些测试** - 选择最相关的测试，让 Claude 编写它们
4. **让 Claude 编写通过测试的代码** - Claude 将迭代实现，直到所有测试通过

这种方法通常会产生更健壮的代码，因为 Claude 有明确的成功标准可以努力实现。

## 实际示例

以下是这些工作流程在实践中的样子。假设你想向现有项目添加一个文档转换工具：

```
// 首先，让 Claude 读取相关文件
> Read the math.py and document.py files

// 然后要求规划（而非实现）
> Plan to implement document_path_to_markdown tool:
1. Create a function that:
   - Takes a file path parameter
   - Validates the file exists
   - Determines file type from extension
   - Reads binary data from file
   - Leverages existing binary_document_to_markdown function
   - Returns markdown string
2. Add appropriate documentation
3. Register the tool with MCP server
4. Add tests

// 最后，要求实现
> Implement the plan
```

然后 Claude 将创建函数、更新必要的文件、编写测试，甚至运行测试套件来验证一切正常工作。

## 其他命令

Claude  Code 包含几个有用的命令：

* `/clear` - 清除对话历史并重置上下文
* `/init` - 扫描代码库并创建 CLAUDE.md 文档
* `#` - 向 CLAUDE.md 文件添加笔记

Claude 还可以处理常规开发任务，如暂存和提交 git 更改、运行测试和管理依赖。你无需在编辑器和终端之间切换，可以让 Claude 处理这些任务，而你专注于更重要的事情。

使用 Claude  Code 成功的关键是记住它被设计为协作伙伴，而不仅仅是代码生成器。你提供的上下文和结构越多，Claude 就能越有效地帮助你构建和维护项目。

# MCP 服务器增强功能

Claude  Code 内置了 MCP 客户端，这意味着你可以连接 MCP 服务器来大幅扩展 Claude 的功能。这为定制你的开发工作流程开启了一些非常强大的可能性。

## MCP 如何扩展 Claude

Model Context Protocol（模型上下文协议）允许 Claude  Code 通过 MCP 服务器连接到外部服务和工具。你不再局限于 Claude 的内置功能，而是可以通过连接提供特定工具、资源或集成的服务器来添加自定义功能。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542913%2F10_-_004_-_Enhancements_with_MCP_Servers_01.1748542913123.jpg)每个 MCP 服务器可以通过三个主要组件向 Claude 暴露不同类型的功能：Tools（用于执行操作）、Prompts（用于模板）和 Resources（用于访问数据）。

## 设置 MCP 服务器

向 Claude  Code 添加 MCP 服务器非常简单。你可以使用命令行来注册服务器：

```
claude mcp add [server-name] [command-to-start-server]
```

例如，如果你有一个通过 `uv run main.py` 启动的文档处理服务器，你可以运行：

```
claude mcp add documents uv run main.py
```

注册后，Claude  Code 将在启动时自动连接到你的服务器。

## 示例：文档处理

一个实际的例子是创建一个让 Claude 读取 PDF 和 Word 文档的工具。通过构建一个带有 "document_path_to_markdown" 工具的 MCP 服务器，你可以让 Claude 将文档内容转换为 markdown 格式。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542914%2F10_-_004_-_Enhancements_with_MCP_Servers_02.1748542913748.jpg)当你让 Claude "将 tests/fixtures/mcp_docs.docx 文件转换为 markdown" 时，它会自动使用你的自定义工具来读取文档并返回转换后的内容。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542914%2F10_-_004_-_Enhancements_with_MCP_Servers_13.1748542914556.jpg)

## 常用 MCP 集成

MCP 生态系统包含许多常见开发工具和服务的服务器：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542915%2F10_-_004_-_Enhancements_with_MCP_Servers_16.1748542915462.jpg)

* **sentry-mcp** - 自动发现并修复 Sentry 中记录的 bug
* **playwright-mcp** - 为 Claude 提供浏览器自动化功能，用于测试和故障排除
* **figma-context-mcp** - 将 Figma 设计暴露给 Claude
* **mcp-atlassian** - 允许 Claude 访问 Confluence 和 Jira
* **firecrawl-mcp-server** - 为 Claude 添加网页抓取功能
* **slack-mcp** - 允许 Claude 发送消息或回复特定线程

## 构建你的开发工作流程

真正的强大之处在于组合多个与你特定开发流程匹配的 MCP 服务器。你可以设置：

* 一个 Sentry 服务器来获取生产环境错误详情
* 一个 Jira 服务器来读取工单需求
* 一个 Slack 服务器在工作完成时通知你的团队
* 为你的内部工具和 API 定制的服务器

这创建了一个开发环境，Claude 可以无缝地与你已经使用的所有工具和服务协作，使其成为一个针对你特定工作流程量身定制的、更加强大的编码助手。

# 并行化 Claude  Code

并行运行多个 Claude  Code 实例是你能实现的最大生产力提升之一。由于 Claude 是轻量级的，你可以轻松启动多个副本，为每个副本分配不同的任务，让它们同时工作。这实际上为你提供了一个虚拟软件工程师团队来处理你的项目。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542981%2F10_-_005_-_Parallelizing_Claude_Code_00.1748542980996.jpg)

## 核心挑战

并行实例的主要问题是文件冲突。当两个 Claude 实例同时尝试修改同一个文件时，它们可能会写入冲突或无效的代码，因为它们彼此不知道对方的更改。

解决方案很简单：给每个实例自己独立的工作空间。每个 Claude 实例使用项目的独立副本工作，在隔离环境中进行更改，然后将这些更改合并回主项目。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542981%2F10_-_005_-_Parallelizing_Claude_Code_02.1748542981591.jpg)

## Git 工作树

Git 工作树（worktrees）是这个工作流程的完美工具。如果你的项目使用 Git（应该使用），你可以立即使用工作树。它们就像 Git 分支系统的扩展，可以在单独的目录中创建项目的完整副本。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542982%2F10_-_005_-_Parallelizing_Claude_Code_03.1748542982035.jpg)每个工作树对应一个独立的分支。你可以拥有：

* 功能 A 分支在一个文件夹中
* 功能 B 分支在另一个文件夹中
* 每个都包含代码库的完整副本
* 在每个工作树中运行独立的 Claude  Code 实例

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542983%2F10_-_005_-_Parallelizing_Claude_Code_04.1748542982398.jpg)当每个 Claude 实例完成工作后，你提交更改并将它们合并回主分支，就像任何正常的 Git 工作流程一样。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542983%2F10_-_005_-_Parallelizing_Claude_Code_05.1748542983427.jpg)

## 自动创建工作树

与其手动创建工作树，你可以让 Claude 处理整个过程。这是一个创建工作树并设置工作空间的提示：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542984%2F10_-_005_-_Parallelizing_Claude_Code_06.1748542984326.jpg)这个提示告诉 Claude：

1. 检查工作树是否已存在
2. 在 `.trees` 文件夹中创建新的 Git 工作树
3. 创建 `.venv` 文件夹的符号链接（因为虚拟环境不被 Git 跟踪）
4. 在该目录中启动新的 Code 实例

## 自定义斜杠命令

重复输入长提示会变得很繁琐。Claude  Code 支持自定义命令来自动化这个过程。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542985%2F10_-_005_-_Parallelizing_Claude_Code_09.1748542984846.jpg)创建自定义命令的步骤：

* 在 `.claude/commands` 目录下添加一个 `.md` 文件
* 在文件中写入你的提示
* 使用 `$ARGUMENTS` 作为动态值的占位符
* 用 `/project:filename argument` 运行

例如，`/project:create_worktree feature_b` 会创建一个名为 "feature_b" 的工作树。

## 并行开发工作流程

以下是典型的并行开发会话的工作方式：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542985%2F10_-_005_-_Parallelizing_Claude_Code_15.1748542985281.jpg)

1. 为不同功能创建多个工作树
2. 在每个工作空间中启动 Claude  Code
3. 为每个实例分配不同的任务
4. 让它们并行工作
5. 每个任务完成后提交更改
6. 将所有分支合并回 main

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542985%2F10_-_005_-_Parallelizing_Claude_Code_16.1748542985628.jpg)

## 自动合并

你还可以用另一个自定义命令来自动化合并过程。创建一个合并提示，它可以：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542986%2F10_-_005_-_Parallelizing_Claude_Code_17.1748542986000.jpg)

1. 进入工作树目录
2. 检查最新的提交
3. 返回根目录
4. 合并工作树分支
5. 自动处理任何合并冲突
6. 根据对更改的理解解决冲突

Claude 甚至可以智能地处理合并冲突，理解来自不同分支的更改上下文并适当地解决它们。

## 扩展你的开发

这种方法可以扩展到你能有效管理的任意数量的并行实例。你唯一的限制是：

* 你机器的资源
* 你协调多个任务的能力
* 潜在合并冲突的复杂性

生产力的提升是巨大的——你不必按顺序处理功能，而是可以同时开发多个功能，大大减少复杂项目的开发时间。

# 自动化调试

Claude  Code 的功能远不止在编辑器中编写代码。它可以监控你部署的应用程序、检测生产环境错误，甚至自动修复它们。这创建了一个强大的工作流程，Claude 充当你的自动化调试助手，捕获那些只在生产环境中出现的问题。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542967%2F10_-_006_-_Automated_Debugging_00.1748542967081.jpg)

## 生产环境问题

这是一个常见的场景：你的应用程序在开发环境中运行完美，但在生产环境中却出问题。你可能有一个聊天机器人在本地能正确响应简单问题，但部署到 AWS Amplify 后却无法生成像电子表格这样的产物。请求看起来成功了，但结果是空的或不完整的。

传统上，你需要翻阅 CloudWatch 日志，搜索错误消息，手动调试本地环境和生产环境之间的差异。这个过程耗时费力，需要你从开发工作切换到运维故障排除。

## 自动错误检测与修复

与其手动调试，你可以设置 Claude 自动处理整个工作流程。以下是系统的工作方式：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542967%2F10_-_006_-_Automated_Debugging_14.1748542967617.jpg)自动化工作流程遵循以下步骤：

1. GitHub Action 每天运行（通常在清晨）
2. Claude 查询 CloudWatch 获取过去 24 小时的错误
3. 它过滤和去重错误以适应上下文限制
4. Claude 分析每个错误并尝试修复
5. 修复的代码被提交，并自动打开一个 Pull Request

## 设置工作流程

GitHub Action 需要几个组件才能有效工作：

* 仓库检出和依赖安装
* Claude  Code 设置和配置
* 安装 AWS CLI 以访问 CloudWatch
* 错误过滤逻辑以管理上下文窗口限制
* 自动提交和创建 Pull Request

当 Claude 在日志中发现错误时，它不仅仅是识别它们——它还理解上下文。例如，如果你有一个只影响生产环境的无效模型标识符（比如 `us.anthropic.claude-3-5-sonnet-20241021-v2:0` 而不是正确的 `us.anthropic.claude-3-5-sonnet-20240624-v1:0`），Claude 可以识别这种模式并应用适当的修复。

## 实际效果

当自动化系统成功运行时，你会看到包含以下内容的 Pull Request：

* 用通俗语言描述的清晰错误说明
* 根本原因分析
* 实施的具体修复
* 更新后的代码，包含正确的模型标识符或配置

Pull Request 成为一个可审查的产物，你可以准确看到 Claude 发现了什么以及它是如何修复的。这让你对更改充满信心，同时保持代码审查实践。

## 自定义调试工作流程

这种自动化调试方法非常灵活。你可以根据具体需求进行调整：

* 调整错误检测频率
* 自定义优先处理哪些类型的错误
* 为你的应用程序添加特定的调试指令
* 集成 CloudWatch 以外的不同日志系统
* 设置关键问题的通知

关键是 Claude  Code 可以理解你应用程序的上下文，智能地分析生产环境错误，并提出考虑到环境特定差异的修复方案。这将调试从被动的手动过程转变为主动的自动化系统，保持你的应用程序平稳运行。

# Computer Use

Computer Use 是一项强大的功能，它让 Claude 能够直接与桌面环境交互，实质上赋予了 AI 像人类一样控制计算机的能力。这项功能为自动化、测试和工作流程辅助开启了全新的可能性。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543021%2F10_-_007_-_Computer_Use_00.1748543021569.jpg)

## Computer Use 能做什么

Claude 不再只是生成代码或提供建议，而是可以实际浏览网站、点击按钮、填写表单，并实时与应用程序交互。这使其对以下任务非常有用：

* Web 应用程序的自动化 QA 测试
* 数据录入和表单填写
* 网站导航和信息收集
* UI 测试和验证
* 重复性桌面任务

## 实际示例：自动化 QA 测试

这里有一个展示 Computer Use 强大功能的实际示例。假设你构建了一个带有自动补全功能的 React 组件——用户可以输入 `@` 来提及文件或资源。乍一看，一切似乎运行正常，但可能存在你尚未发现的边缘情况。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543022%2F10_-_007_-_Computer_Use_05.1748543022086.jpg)与其手动测试每种可能的交互，你可以将这项工作委托给 Claude。你只需提供如下指令：

```
Your goal is to conduct QA testing on a React component hosted at https://test-mentioner.vercel.app/

Testing process:
1. Open a new browser tab
2. Navigate to https://test-mentioner.vercel.app/
3. Execute the test cases below one by one
4. After completing all tests, write a concise report

Test cases:
1. Typing 'Did you read @' should display autocomplete options
2. Typing 'Did you read @' then pressing enter should add '@document.pdf'
3. After adding '@document.pdf', pressing backspace should show autocomplete options directly below the text, not elsewhere on the page
```

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543022%2F10_-_007_-_Computer_Use_16.1748543022490.jpg)

## 实际工作原理

Computer Use 在受控环境中运行——通常是一个带有浏览器的 Docker 容器，与你的主系统完全隔离。你通过聊天界面与 Claude 交互，告诉它要做什么，然后观察它导航和与应用程序交互。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543023%2F10_-_007_-_Computer_Use_17.1748543022870.jpg)Claude 逐步遵循你的指令，截取屏幕截图、点击元素、输入文本并观察结果。在 QA 测试示例中，Claude 会：

1. 导航到指定的 URL
2. 输入测试内容并观察自动补全行为
3. 测试回车键功能
4. 检查退格键行为以确保正确定位
5. 生成详细报告，说明哪些通过了，哪些失败了

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543023%2F10_-_007_-_Computer_Use_18.1748543023770.jpg)

## 结果

在运行完所有测试用例后，Claude 会提供一份全面的报告。在我们的示例中，它可能发现前两个测试通过了（自动补全正确显示，回车键正常工作），但第三个测试失败了，因为按下退格键时自动补全下拉框出现在了错误的位置。

这种自动化测试可以为开发人员节省大量时间，特别是对于重复性的 QA 任务或当你需要快速测试多个场景时。你不必手动点击每一个可能的交互，而是可以描述你想测试的内容，让 Claude 处理执行。

## 安全与隔离

Computer Use 在沙盒环境中运行以确保安全。浏览器和桌面环境在 Docker 容器内运行，与你的主系统完全隔离。这意味着 Claude 可以与 Web 应用程序交互并测试界面，而不会对你的个人文件或系统安全造成任何风险。

这种隔离至关重要，因为它允许你给予 Claude 广泛的权限来与应用程序交互，同时保持对它可以访问和不能访问的内容的完全控制。

# Computer Use 工作原理

Claude 中的 Computer Use 与常规工具使用的工作方式完全相同——它只是同一底层工具系统的特殊实现。理解这种联系使 Computer Use 更容易理解和实现。

## 工具使用回顾

在深入了解 Computer Use 之前，让我们快速回顾一下常规工具使用在 Claude 中的工作方式：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543025%2F10_-_008_-_How_Computer_Use_Works_01.1748543025424.jpg)

1. 你向 Claude 发送用户消息以及工具模式
2. Claude 决定需要使用工具来回答问题
3. Claude 返回一个工具使用请求，包含工具名称和输入参数
4. 你的服务器运行实际函数并返回结果
5. 你将结果以工具结果消息的形式发送回 Claude

例如，如果有人问"旧金山的天气怎么样？"，你需要提供一个 `get_weather` 工具模式。Claude 会使用位置参数调用该工具，你的代码获取天气数据，然后你将"晴天"返回给 Claude。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543026%2F10_-_008_-_How_Computer_Use_Works_07.1748543026297.jpg)

## Computer Use：相同流程，不同工具

Computer Use 遵循完全相同的模式。关键的洞察是 Computer Use 被实现为一个工具——只是一个非常特殊的工具，可以与桌面环境交互。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543026%2F10_-_008_-_How_Computer_Use_Works_08.1748543026655.jpg)以下是发生的过程：

* 你包含一个提供计算机交互能力的工具模式
* Claude 决定使用计算机工具
* 你不是运行一个简单的函数，而是在计算环境中执行请求的操作
* 你将结果（如屏幕截图）发送回 Claude

## 计算机工具模式

Computer Use 工具模式一开始很简单，但会自动扩展为更全面的内容：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543027%2F10_-_008_-_How_Computer_Use_Works_09.1748543027109.jpg)你发送一个基本模式，如：

```
{
  "type": "computer_20250124",
  "name": "computer",
  "display_width_px": 1024,
  "display_height_px": 768,
  "display_number": 1
}
```

在后台，这会被扩展为一个详细的模式，告诉 Claude 它可以执行以下操作：

* `key` - 按键盘按键
* `mouse_move` - 移动光标
* `left_click` - 在特定坐标点击
* `screenshot` - 截取屏幕截图
* `scroll` - 滚动屏幕

## 计算环境

要使 Computer Use 工作，你需要一个实际的计算环境来以编程方式执行这些操作。最常见的方法是使用带有桌面环境（如 Firefox）的 Docker 容器。

当 Claude 请求一个操作，如"在坐标 (500, 300) 处点击"时，你的系统会：

1. 接收工具使用请求
2. 在 Docker 容器中执行鼠标点击
3. 截取结果的屏幕截图
4. 将屏幕截图发送回 Claude

Docker 容器不需要很复杂——它只需要支持编程式的键盘和鼠标交互。

## 入门指南

你不需要从头构建计算环境。Anthropic 提供了一个参考实现，处理所有技术细节。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543027%2F10_-_008_-_How_Computer_Use_Works_17.1748543027671.jpg)设置很简单：

1. 安装 Docker（你可能已经安装了）
2. 使用你的 API 密钥运行提供的 Docker 命令
3. 访问 Web 界面与 Claude 聊天

设置命令如下：

```
export ANTHROPIC_API_KEY="your_api_key"
docker run \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -v $HOME/.anthropic:/home/computeruse/.anthropic \
  -p 5900:5900 \
  -p 8501:8501 \
  -p 6080:6080 \
  -p 8080:8080 \
  -it ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest
```

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543028%2F10_-_008_-_How_Computer_Use_Works_19.1748543027991.jpg)运行后，你将可以访问一个聊天界面，直接测试 Claude 的 Computer Use 功能。完整的设置指南可在 github.com/anthropics/anthropic-quickstarts 上获取。

## 关键要点

Computer Use 并不神奇——它只是将常规工具使用系统应用于桌面自动化。Claude 并不直接控制计算机；相反，它发出工具请求，由你的代码在受控环境中执行操作来完成。这使得 Computer Use 既强大又安全，因为你对实际执行的操作保持完全控制。
