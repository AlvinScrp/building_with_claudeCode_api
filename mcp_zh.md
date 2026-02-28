# MCP 简介

模型上下文协议（MCP）是一个通信层，它为 Claude 提供上下文和工具，而无需你编写大量繁琐的集成代码。可以将其理解为一种将工具定义和执行的负担从你的服务器转移到专门的 MCP 服务器的方式。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542645%2F09_-_001_-_Introducing_MCP_01.1748542645351.jpg)当你第一次接触 MCP 时，你会看到展示基本架构的图表：一个 MCP 客户端（你的服务器）连接到包含工具、提示词和资源的 MCP 服务器。每个 MCP 服务器充当某个外部服务的接口。

## 通过实际示例理解 MCP

假设你正在构建一个聊天界面，用户可以向 Claude 询问他们的 GitHub 数据。用户可能会问"我所有仓库中有哪些待处理的拉取请求？"要回答这个问题，Claude 需要访问 GitHub API 的工具。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542646%2F09_-_001_-_Introducing_MCP_04.1748542645841.jpg)如果没有 MCP，你需要自己创建所有的 GitHub 集成工具。这意味着要为你想支持的每一项 GitHub 功能编写模式定义和函数。

## 工具函数问题

GitHub 的功能非常庞大——仓库、拉取请求、议题、项目等等。要构建一个完整的 GitHub 聊天机器人，你需要编写数量惊人的工具：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542646%2F09_-_001_-_Introducing_MCP_05.1748542646307.jpg)每个工具都需要模式定义和函数实现。作为开发者，这代表着大量需要编写、测试和维护的代码。

## MCP 如何解决这个问题

MCP 将工具定义和执行的负担从你的服务器转移到 MCP 服务器。不需要你自己编写所有 GitHub 工具，它们在专用的 MCP 服务器内部被编写和执行。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542646%2F09_-_001_-_Introducing_MCP_08.1748542646653.jpg)MCP 服务器充当 GitHub 功能的包装器，提供预构建的工具，你无需自己实现即可使用。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542647%2F09_-_001_-_Introducing_MCP_09.1748542647009.jpg)MCP 服务器提供对外部服务实现的数据或功能的访问。它们将复杂的集成封装成可复用的组件，任何应用程序都可以连接使用。

## 关于 MCP 的常见问题

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542647%2F09_-_001_-_Introducing_MCP_12.1748542647366.jpg)

### 谁来编写 MCP 服务器？

任何人都可以创建 MCP 服务器实现。通常，服务提供商自己会制作官方的 MCP 实现。例如，AWS 可能会发布一个包含其各种服务工具的官方 MCP 服务器。

### MCP 与直接 API 调用有什么不同？

MCP 服务器提供已经为你定义好的工具模式和函数。如果你直接调用 API，则需要自己编写这些工具定义。MCP 为你省去了这些实现工作。

### MCP 不就是工具使用吗？

这是一个常见的误解。MCP 服务器和工具使用是互补但不同的概念。MCP 关注的是谁来完成创建和维护工具的工作。使用 MCP 时，别人已经为你编写了工具函数和模式——它们被封装在 MCP 服务器内部。

关键的理解是，MCP 服务器提供已经为你定义好的工具模式和函数，消除了自己构建和维护复杂集成的需要。

# MCP 客户端

MCP 客户端充当你的服务器与 MCP 服务器之间的通信桥梁。可以将其视为你访问 MCP 服务器所提供的所有工具的入口。当你需要使用外部工具或服务时，客户端会为你处理所有的消息传递和协议细节。

## 传输无关的通信

MCP 的一个关键优势是传输无关性——通俗地说，就是客户端和服务器可以使用不同的通信方式相互通信。最常见的设置是将 MCP 客户端和服务器运行在同一台机器上，通过标准输入/输出进行通信。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542644%2F09_-_002_-_MCP_Clients_01.1748542644766.jpg)但你并不局限于这种方式。MCP 客户端和服务器还可以通过以下方式连接：

* HTTP
* WebSocket
* 各种其他网络协议

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542645%2F09_-_002_-_MCP_Clients_03.1748542645442.jpg)

## 消息类型

连接建立后，客户端和服务器会交换 MCP 规范中定义的特定消息类型。你将使用的主要消息类型有：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542645%2F09_-_002_-_MCP_Clients_04.1748542645814.jpg)**ListToolsRequest/ListToolsResult：** 客户端向服务器询问"你提供哪些工具？"并获取可用工具列表。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542646%2F09_-_002_-_MCP_Clients_05.1748542646228.jpg)**CallToolRequest/CallToolResult：** 客户端请求服务器使用特定参数运行某个工具，然后接收结果。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542646%2F09_-_002_-_MCP_Clients_06.1748542646636.jpg)

## 完整流程示例

下面展示在真实场景中所有组件是如何协同工作的。假设用户问"我有哪些仓库？"——以下是完整的通信流程：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542647%2F09_-_002_-_MCP_Clients_08.1748542647060.jpg)流程从用户向你的服务器提交查询开始。你的服务器意识到在发起请求之前，需要先向 Claude 提供可用工具列表。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542648%2F09_-_002_-_MCP_Clients_09.1748542647956.jpg)你的服务器向 MCP 客户端请求工具，客户端向 MCP 服务器发送 `ListToolsRequest` 并接收返回的 `ListToolsResult`。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542648%2F09_-_002_-_MCP_Clients_11.1748542648353.jpg)现在你的服务器拥有了向 Claude 发起初始请求所需的一切——用户的问题和可用工具。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542649%2F09_-_002_-_MCP_Clients_12.1748542648890.jpg)Claude 检查工具并决定需要调用其中一个来回答问题。它返回一个工具使用请求。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542649%2F09_-_002_-_MCP_Clients_14.1748542649299.jpg)你的服务器请求 MCP 客户端执行 Claude 所请求的工具。MCP 客户端向 MCP 服务器发送 `CallToolRequest`，MCP 服务器随后向 GitHub 发起实际请求。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542649%2F09_-_002_-_MCP_Clients_15.1748542649806.jpg)GitHub 返回仓库数据，数据通过 MCP 服务器作为 `CallToolResult` 回传，再到 MCP 客户端，最终到达你的服务器。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542650%2F09_-_002_-_MCP_Clients_17.1748542650158.jpg)你的服务器在后续消息中将工具结果发回给 Claude。此时 Claude 拥有了生成完整回复所需的全部信息。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542651%2F09_-_002_-_MCP_Clients_18.1748542650970.jpg)最后，Claude 返回格式化的答案，你的服务器将其传递给用户。

是的，这个流程涉及很多步骤，但每个组件都有明确的职责。MCP 客户端抽象了服务器通信的复杂性，让你可以专注于构建应用逻辑。当我们实现自己的 MCP 客户端和服务器时，你将看到每个部分在实践中是如何组合在一起的。

# 项目设置

我们将构建一个基于命令行的聊天机器人，以更好地理解 MCP 客户端和服务器如何协同工作。这个动手项目将为你提供 MCP 架构两端的实践经验。

## 我们要构建什么

我们的聊天机器人将允许用户通过命令行界面与一组文档进行交互。系统由两个主要组件组成：

* 一个处理用户交互的 MCP 客户端
* 一个管理文档操作的自定义 MCP 服务器

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542682%2F09_-_003_-_Project_Setup_03.1748542682857.jpg)

服务器将提供两个基本工具：一个用于读取文档内容，另一个用于更新文档。为了简单起见，所有文档将存储在内存中——不需要数据库。

## 重要的架构说明

在实际项目中，你通常只实现 MCP 客户端或 MCP 服务器，而不是两者都实现。你可能会创建：

* 一个 MCP 服务器，将你的服务暴露给其他开发者
* 一个 MCP 客户端，连接到现有的 MCP 服务器

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542683%2F09_-_003_-_Project_Setup_07.1748542683236.jpg)

我们在本项目中同时构建两个组件纯粹是出于教学目的——为了理解它们如何通信和协同工作。

## 项目设置

下载本课程附带的 `cli_project.zip` 文件，并将其解压到你偏好的开发目录。在项目文件夹中打开你的代码编辑器。

项目包含一个详尽的 README 文件，其中有设置说明。按照以下步骤操作：

1. 将你的 Anthropic API 密钥添加到 `.env` 文件中
2. 使用 UV（推荐）或 pip 安装依赖
3. 运行启动应用程序以验证一切正常

## 运行应用程序

在终端中导航到你的项目目录。你会看到主要的项目文件，包括 `main.py`、`mcp_client.py` 和 `mcp_server.py`。

要启动应用程序，使用以下命令之一：

```
# 如果使用 UV（推荐）
uv run main.py

# 如果使用标准 Python
python main.py
```

当应用程序成功启动后，你会看到一个聊天提示符。通过询问一个简单的问题（如"1+1等于几？"）来测试它——你应该会从 Claude 得到一个快速回复。

基本设置完成后，我们就可以开始实现 MCP 功能，并探索客户端和服务器如何通过模型上下文协议进行通信了。

## 使用 MCP 定义工具

使用官方 Python SDK 构建 MCP 服务器会变得简单得多。SDK 通过装饰器和类型提示为你处理所有复杂性，而无需手动编写复杂的 JSON 模式。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542694%2F09_-_004_-_Defining_Tools_with_MCP_00.1748542693957.jpg)在这个示例中，我们正在创建一个管理存储在内存中的文档的 MCP 服务器。服务器将提供两个基本工具：一个用于读取文档内容，另一个用于通过查找替换操作来更新文档。

## 设置 MCP 服务器

Python MCP SDK 使服务器创建变得非常简单。你只需一行代码就可以初始化一个完整的 MCP 服务器：

```
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")
```

在此实现中，文档存储在一个简单的 Python 字典中，键是文档 ID，值包含文档内容：

```
docs = {
     "deposition.md": "这份证词记录涵盖了 Angela Smith（注册工程师 P.E.）的证言。",
    "report.pdf": "该报告详细说明了一座 20 米冷凝塔的状况。",
    "financials.docx": "这份财务资料概述了项目的预算和支出。",
    "outlook.pdf": "本文件展示了对未来绩效的预测。",
    "plan.md": "该计划概述了项目实施的步骤。",
    "spec.txt": "这些规格说明定义了设备的技术要求。"
}
```

## 使用装饰器定义工具

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542694%2F09_-_004_-_Defining_Tools_with_MCP_05.1748542694369.jpg)SDK 将工具创建从一个冗长的过程转变为简洁易读的代码。你不再需要编写冗长的 JSON 模式，而是使用 Python 装饰器和类型提示。

## 创建文档读取工具

第一个工具允许 Claude 通过文档 ID 读取任何文档。以下是完整实现：

```
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]
```

`@mcp.tool` 装饰器会自动生成 Claude 所需的 JSON 模式。Pydantic 的 `Field` 类提供参数描述，帮助 Claude 理解每个参数期望的内容。

## 构建文档编辑工具

第二个工具对文档执行简单的查找替换操作：

```
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
```

该工具接受三个参数：文档 ID、要查找的文本和替换文本。实现使用了 Python 内置的字符串 `replace()` 方法以保持简单。

## 错误处理

两个工具都包含基本的错误处理，用于管理 Claude 请求不存在的文档的情况。当提供无效的文档 ID 时，工具会抛出一个 `ValueError`，附带描述性消息，Claude 可以理解并据此采取行动。

## SDK 方式的主要优势

* 从 Python 类型提示自动生成 JSON 模式
* 简洁、易读、易于维护的代码
* 通过 Pydantic 内置参数验证
* 与手动编写模式相比减少了样板代码
* 类型安全和 IDE 开发支持

MCP Python SDK 将曾经复杂的工具定义编写过程转变为对 Python 开发者来说自然而然的事情。你只需专注于业务逻辑，SDK 会处理协议细节。

# 服务器检查器

在构建 MCP 服务器时，你需要一种方法来测试功能，而无需连接到完整的应用程序。Python MCP SDK 包含一个内置的基于浏览器的检查器，让你可以实时调试和测试服务器。

## 启动检查器

首先，确保你的 Python 环境已激活（查看项目的 README 以获取确切命令）。然后使用以下命令运行检查器：

```
mcp dev mcp_server.py
```

这将在端口 6277 上启动一个开发服务器，并给你一个本地 URL 在浏览器中打开。检查器界面将加载，显示 MCP Inspector 仪表板。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542727%2F09_-_005_-_The_Server_Inspector_05.1748542726831.jpg)

## 关于界面的重要说明

MCP 检查器正在积极开发中，因此你看到的界面可能与当前截图不同。但是，测试工具、资源和提示词的核心功能应该保持类似。

## 连接和测试工具

点击左侧的"Connect"按钮启动你的 MCP 服务器。连接成功后，你会看到一个导航栏，包含 Resources、Prompts、Tools 和其他功能的部分。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542727%2F09_-_005_-_The_Server_Inspector_07.1748542727369.jpg)测试工具的步骤：

* 导航到 Tools 部分
* 点击"List Tools"查看所有可用工具
* 选择一个工具打开其测试界面
* 填写所需参数
* 点击"Run Tool"执行并查看结果

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542728%2F09_-_005_-_The_Server_Inspector_09.1748542727826.jpg)

## 测试文档操作

例如，要测试文档读取工具，你需要输入文档 ID（如"deposition.md"）并运行该工具。检查器会显示结果，包括任何返回的内容或成功消息。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542728%2F09_-_005_-_The_Server_Inspector_17.1748542728249.jpg)你可以链式执行操作来验证功能。例如，在通过替换文本编辑文档后，你可以立即再次运行读取工具，确认更改已正确应用。

## 开发工作流

检查器创建了一个高效的开发循环：

* 修改你的 MCP 服务器代码
* 通过检查器测试单个工具
* 无需完整的应用程序设置即可验证结果
* 隔离调试问题

当你构建更复杂的 MCP 服务器时，这个工具变得不可或缺。它消除了仅为测试基本功能就需要将服务器连接到 Claude 或其他应用程序的需要，使开发更快速、更专注。

# 实现客户端

现在我们的 MCP 服务器已经可以工作了，是时候构建客户端了。客户端是让我们的应用程序能够与 MCP 服务器通信并访问其功能的组件。

## 理解客户端架构

在大多数实际项目中，你只会实现 MCP 客户端或 MCP 服务器——而不是两者都实现。我们在本项目中同时构建两者，只是为了让你看到它们如何协同工作。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542735%2F09_-_006_-_Implementing_a_Client_01.1748542735212.jpg)MCP 客户端由两个主要组件组成：

* **MCP Client** - 我们创建的自定义类，用于更方便地使用会话
* **Client Session** - 与服务器的实际连接（MCP Python SDK 的一部分）

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542735%2F09_-_006_-_Implementing_a_Client_02.1748542735805.jpg)客户端会话在使用完毕后需要进行适当的资源清理。这就是我们将其封装在自定义 MCP Client 类中的原因——自动处理所有清理工作。

## 客户端如何融入我们的应用程序

还记得我们的应用程序流程吗？我们的 CLI 代码需要与 MCP 服务器进行两项主要操作：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542736%2F09_-_006_-_Implementing_a_Client_06.1748542736441.jpg)

* 1. 获取可用工具列表以发送给 Claude
  2. 当 Claude 请求时执行工具

MCP 客户端通过简单的方法调用提供这些功能，我们的应用程序代码可以直接使用。

## 实现核心方法

我们需要在客户端中实现两个关键方法：`list_tools()` 和 `call_tool()`。

### List Tools 方法

该方法从服务器获取所有可用工具：

```
async def list_tools(self) -> list[types.Tool]:
    result = await self.session().list_tools()
    return result.tools
```

很简单——我们访问会话（与服务器的连接），调用内置的 `list_tools()` 函数，并返回结果中的工具。

### Call Tool 方法

该方法在服务器上执行特定工具：

```
async def call_tool(
    self, tool_name: str, tool_input: dict
) -> types.CallToolResult | None:
    return await self.session().call_tool(tool_name, tool_input)
```

我们将工具名称和输入参数（由 Claude 提供）传递给服务器并返回结果。

## 测试客户端

要测试我们的实现，可以直接运行客户端。文件中包含一个测试工具，它连接到我们的 MCP 服务器并调用我们的方法：

```
async with MCPClient(
    command="uv", args=["run", "mcp_server.py"]
) as client:
    result = await client.list_tools()
    print(result)
```

运行此测试时，我们应该看到工具定义被打印出来，包括我们之前创建的 `read_doc_contents` 和 `edit_document` 工具。

## 将所有部分组合在一起

现在我们的客户端可以列出工具并调用它们了，我们可以测试完整的流程。当我们运行主应用程序并向 Claude 询问某个文档时：

1. 我们的代码使用客户端获取可用工具
2. 这些工具连同用户的问题一起发送给 Claude
3. Claude 决定使用 `read_doc_contents` 工具
4. 我们的代码使用客户端执行该工具
5. 结果被发回给 Claude，Claude 随后回复用户

例如，询问"report.pdf 文档的内容是什么？"将触发 Claude 使用我们的文档读取工具，我们将获取到关于我们在服务器中设置的 20m 冷凝塔文档的信息。

客户端充当应用程序逻辑和 MCP 服务器之间的桥梁，使访问服务器功能变得简单，无需担心底层连接细节。

# 定义资源

MCP 服务器中的资源允许你向客户端暴露数据，类似于典型 HTTP 服务器中的 GET 请求处理程序。它们非常适合需要获取信息而非执行操作的场景。

## 通过示例理解资源

假设你想构建一个文档提及功能，用户可以输入 `@document_name` 来引用文件。这需要两个操作：

* 获取所有可用文档的列表（用于自动补全）
* 获取特定文档的内容（当被提及时）

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542781%2F09_-_007_-_Defining_Resources_01.1748542781089.jpg)当用户输入 `@` 时，你需要显示可用文档。当他们提交包含提及的消息时，你自动将该文档的内容注入发送给 Claude 的提示词中。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542782%2F09_-_007_-_Defining_Resources_03.1748542782123.jpg)

## 资源如何工作

资源遵循请求-响应模式。你的客户端发送一个带有 URI 的 `ReadResourceRequest`，MCP 服务器响应数据。URI 就像你要访问的资源的地址。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542783%2F09_-_007_-_Defining_Resources_04.1748542783045.jpg)

## 资源类型

资源有两种类型：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542783%2F09_-_007_-_Defining_Resources_07.1748542783391.jpg)* **直接资源：** 不变的静态 URI，如 `docs://documents`

* **模板资源：** 带参数的 URI，如 `docs://documents/{doc_id}`

对于模板资源，Python SDK 会自动从 URI 中解析参数，并将它们作为关键字参数传递给你的函数。

## 实现资源

资源使用 `@mcp.resource()` 装饰器定义。以下是创建两种类型的方法：

### 直接资源（列出文档）

```
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())
```

### 模板资源（获取文档）

```
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
```

## MIME 类型

资源可以返回任何类型的数据——字符串、JSON、二进制等。`mime_type` 参数为客户端提供关于你返回的数据类型的提示：

* `application/json` - 结构化 JSON 数据
* `text/plain` - 纯文本内容
* 其他任何有效的 MIME 类型用于不同的数据格式

MCP Python SDK 会自动序列化你的返回值。你不需要手动转换为 JSON 字符串。

## 测试资源

你可以使用 MCP Inspector 测试你的资源。使用以下命令运行服务器：

```
uv run mcp dev mcp_server.py
```

然后在浏览器中连接到检查器。你会看到：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542784%2F09_-_007_-_Defining_Resources_17.1748542783889.jpg)* **Resources：** 列出你的直接/静态资源

* **Resource Templates：** 显示接受参数的模板资源

点击任何资源进行测试，查看客户端将收到的确切响应结构。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542784%2F09_-_007_-_Defining_Resources_18.1748542784293.jpg)

## 要点总结

* 资源暴露数据，工具执行操作
* 对静态数据使用直接资源，对参数化查询使用模板资源
* MIME 类型帮助客户端理解响应格式
* SDK 自动处理序列化
* 模板 URI 中的参数名称成为函数参数

资源提供了一种简洁的方式，让数据可供 MCP 客户端使用，支持文档提及、文件浏览等功能，或任何需要从服务器获取信息的场景。

# 访问资源

MCP 中的资源允许你的服务器暴露可以直接包含在提示词中的数据，而不需要通过工具调用来访问信息。这为向 Claude 等 AI 模型提供上下文创造了一种更高效的方式。

## 理解资源请求

当你在 MCP 服务器上定义了资源后，你的客户端需要一种方式来请求和使用它们。客户端充当应用程序和 MCP 服务器之间的桥梁，自动处理通信和数据解析。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542773%2F09_-_008_-_Accessing_Resources_00.1748542772895.jpg)流程很简单：当用户想要引用一个文档时（如输入"@report.pdf"），你的应用程序使用 MCP 客户端从服务器获取该资源，并将其内容直接包含在发送给 Claude 的提示词中。

## 实现资源读取

核心功能需要在 MCP 客户端中实现一个 `read_resource` 函数。该函数接受一个 URI 参数，用于标识要获取的资源：

```
async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]
```

MCP 服务器的响应包含一个 `contents` 列表。你通常只需要第一个元素，它包含实际的资源数据以及 MIME 类型等元数据。

## 处理不同的内容类型

资源可以返回不同类型的内容，因此你的客户端需要适当地解析它们。MIME 类型告诉你如何处理数据：

```
if isinstance(resource, types.TextResourceContents):
    if resource.mimeType == "application/json":
        return json.loads(resource.text)

    return resource.text
```

这种方法确保 JSON 资源被正确解析为 Python 对象，而纯文本资源以字符串形式返回。MIME 类型充当确定正确解析策略的提示。

## 所需的导入

要使其正常工作，你需要在 MCP 客户端中添加以下导入：

```
import json
from pydantic import AnyUrl
```

`json` 模块处理 JSON 响应的解析，而 `AnyUrl` 确保 URI 参数的正确类型处理。

## 测试资源访问

实现完成后，你可以通过 CLI 应用程序测试功能。当你输入类似"@report.pdf 文档里有什么内容？"时，系统应该：

* 在自动补全列表中显示可用资源
* 允许你选择一个资源
* 自动获取资源内容
* 将该内容包含在发送给 Claude 的提示词中

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542774%2F09_-_008_-_Accessing_Resources_09.1748542773725.jpg)关键优势在于 Claude 直接在提示词中接收文档内容，无需通过工具调用来访问信息。这使得交互更快速、更高效。

## 与应用程序集成

记住，你编写的 MCP 客户端代码会被应用程序的其他部分使用。`read_resource` 函数成为一个构建模块，其他组件可以调用它来获取文档内容、列出可用资源或将资源数据集成到提示词中。

这种关注点分离使你的代码保持整洁：MCP 客户端处理与服务器的通信，而应用程序逻辑专注于如何有效地使用这些数据。

# 定义提示词

MCP 服务器中的提示词让你可以定义预构建的、高质量的指令，客户端可以直接使用，而无需从头编写自己的提示词。可以将它们视为精心制作的模板，能比用户自己想出的提示词产生更好的结果。

## 为什么使用提示词？

假设你想让 Claude 将文档重新格式化为 Markdown。用户可以直接输入"将 report.pdf 转换为 markdown"，这样也能工作。但如果使用经过充分测试的提示词，其中包含关于格式、结构和输出要求的具体指令，他们很可能会得到更好的结果。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542823%2F09_-_009_-_Defining_Prompts_07.1748542822992.jpg)关键的洞察是，虽然用户可以自己完成这些任务，但使用由 MCP 服务器作者精心开发和测试的提示词，他们会获得更一致、更高质量的结果。

## 提示词如何工作

提示词定义了一组用户和助手消息，客户端可以直接使用。当客户端请求一个提示词时，你的服务器返回一个可以直接发送给 Claude 的消息列表。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542823%2F09_-_009_-_Defining_Prompts_08.1748542823609.jpg)基本结构如下：

* 使用 `@mcp.prompt()` 装饰器定义提示词
* 为每个提示词添加名称和描述
* 返回构成完整提示词的消息列表
* 这些提示词应该是高质量的、经过充分测试的，并且与你的 MCP 服务器的目的相关

## 构建格式化命令

以下是如何实现文档格式化提示词。首先，你需要导入基础消息类型：

```
from mcp.server.fastmcp import base
```

然后定义你的提示词函数：

```
@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
你的目标是将一个文档重新排版为使用 Markdown 语法编写的格式。
你需要重新排版的文档 ID 是：
根据需要添加标题、项目符号、表格等内容。可以自由添加额外的格式。
使用 edit_document 工具来编辑该文档。在文档完成重新排版之后……
"""

    return [
        base.UserMessage(prompt)
    ]
```

## 测试你的提示词

你可以使用 MCP Inspector 测试提示词。导航到 Prompts 部分，选择你的提示词，并提供所需的参数。检查器会显示将发送给 Claude 的生成消息。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542824%2F09_-_009_-_Defining_Prompts_18.1748542824116.jpg)这让你可以在实际应用中使用之前，验证提示词是否正确插值变量并产生预期的消息结构。

## 最佳实践

为你的 MCP 服务器创建提示词时：

* 专注于与服务器目的密切相关的任务
* 编写详细、具体的指令，而非模糊的请求
* 用不同的输入充分测试你的提示词
* 包含清晰的描述，让用户了解每个提示词的功能
* 考虑提示词如何与服务器的工具和资源配合使用

记住，提示词旨在提供用户自己不容易获得的价值——它们应该代表你在 MCP 服务器所覆盖领域的专业知识。

# 客户端中的提示词

MCP 中的提示词定义了一组用户和助手消息，可供客户端使用。这些提示词应该是高质量的、经过充分测试的，并且与 MCP 服务器的整体目的相关。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542819%2F09_-_010_-_Prompts_in_the_Client_17.1748542819284.jpg)

## 实现 List Prompts

第一步是在 MCP 客户端中实现 `list_prompts` 方法。该方法从服务器检索所有可用的提示词：

```
async def list_prompts(self) -> list[types.Prompt]:
    result = await self.session().list_prompts()
    return result.prompts
```

这个简单的实现调用会话的 `list_prompts` 方法，并返回结果中的 prompts 数组。

## 获取单个提示词

`get_prompt` 方法检索一个特定的提示词，并将参数插值进去。当你请求一个提示词时，你提供的参数会作为关键字参数传递给提示词函数：

```
async def get_prompt(self, prompt_name, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

该方法返回结果中的消息，这些消息构成一个可以直接输入给 Claude 的对话。

## 提示词参数如何工作

当你在服务器端定义提示词函数时，它可以接受参数。例如，文档格式化提示词可能需要一个 `doc_id` 参数：

```
def format_document(doc_id: str):
    # doc_id 被插值到提示词中
```

当客户端调用 `get_prompt` 时，参数字典应包含期望的键。MCP 服务器会将这些作为关键字参数传递给提示词函数，允许动态内容被插入到提示词模板中。

## 在 CLI 中测试提示词

实现完成后，你可以通过命令行界面测试提示词。当你输入斜杠时，可用的提示词会作为命令出现。选择一个提示词后，可能会提示你从可用选项中选择（如文档 ID），然后完整的提示词会发送给 Claude。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542819%2F09_-_010_-_Prompts_in_the_Client_11.1748542819808.jpg)工作流程如下：

1. 用户选择一个提示词（如"format"）
2. 系统提示输入所需参数（如要格式化哪个文档）
3. 提示词连同插值后的值一起发送给 Claude
4. Claude 然后可以使用工具获取额外数据并完成任务

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542820%2F09_-_010_-_Prompts_in_the_Client_15.1748542820224.jpg)

## 提示词最佳实践

为你的 MCP 服务器创建提示词时：

* 使其与服务器的目的相关
* 部署前充分测试
* 使用清晰、具体的指令
* 设计时考虑与可用工具的良好配合
* 考虑用户需要提供哪些参数

提示词弥合了预定义功能和动态用户需求之间的差距，为 Claude 提供了处理复杂任务的结构化起点，同时通过参数化保持灵活性。
