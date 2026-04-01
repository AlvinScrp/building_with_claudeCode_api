# Agent 与 Workflow

Workflow 和 Agent 是处理用户任务的策略，适用于 Claude 无法在单次请求中完成的任务。实际上，你在整个课程中已经创建过两者——当你使用 Tool 并让 Claude 自己决定如何完成任务时，那就是一个 Agent。

## 何时使用 Workflow vs Agent

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543103%2F11_-_001_-_Agents_and_Workflows_01.1748543103044.jpg)这个决定取决于你对任务的理解程度：

* **使用 Workflow**：当你能够清晰地想象出 Claude 解决问题应该经过的确切流程或步骤时，或者当你的应用 UX 将用户限制在一组特定任务中时
* **使用 Agent**：当你不确定要给 Claude 什么任务或任务参数时

Workflow 是一系列调用 Claude 的过程，旨在通过预定的一系列步骤解决特定问题。Agent 则是给 Claude 一个目标和一组 Tool，期望 Claude 通过提供的 Tool 自行决定如何完成目标。

## 示例：图像转 CAD Workflow

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543103%2F11_-_001_-_Agents_and_Workflows_06.1748543103613.jpg)让我们看一个实际的 Workflow 示例。假设构建一个 Web 应用，用户拖放一张金属零件的图像，然后你从中创建一个 STEP 文件（3D 模型的行业标准）。

由于我们对用户提供图像文件后该做什么有相当清晰的了解，而且我们可以很容易地将这一切作为预定义的一系列步骤用代码写出来，这就成为了一个完美的 Workflow 候选。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543104%2F11_-_001_-_Agents_and_Workflows_07.1748543103955.jpg)Workflow 分解如下：

1. 将图像输入 Claude，要求它描述该对象
2. 根据描述，要求 Claude 使用 CadQuery 库对该对象建模
3. 创建渲染图
4. 要求 Claude 将渲染图与原始图像进行评分。如果有问题，进行修复

## 评估器-优化器模式

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543104%2F11_-_001_-_Agents_and_Workflows_15.1748543104283.jpg)这个建模 Workflow 是评估器-优化器模式的一个示例。它的工作原理如下：

* **生产者**：接收输入并创建输出（Claude 使用 CadQuery 对零件建模并创建渲染图）
* **评分者**：根据某些标准评估输出
* **反馈循环**：如果评分者不接受输出，反馈会返回给生产者进行改进
* **迭代**：循环重复直到评分者接受输出

## 为什么要学习 Workflow 模式

识别不同 Workflow 的目标是为你提供一组可重复的配方，用于实现自己的功能。评估器-优化器是一种对其他工程师来说效果很好的 Workflow 模式——考虑在你自己的应用中使用它！

记住，识别 Workflow 本身并不会为我们带来任何实际效果——我们仍然需要编写实际的代码来实现它们。但这些模式已经被许多工程师证明是成功的，所以它们值得理解并应用到你自己的项目中。

# 并行化 Workflow

在构建 AI 应用时，你经常会遇到表面上看起来很简单，但当你尝试有效实现时却变得复杂的任务。让我们探索一种称为并行化 Workflow 的强大模式，它可以帮助你将复杂任务分解为可管理的、专注的部分。

## 复杂单一提示词的问题

假设你正在构建一个材料设计应用，用户上传零件图像并获得最佳材料使用建议。你的第一直觉可能是将图像发送给 Claude，并附带一个简单的提示词，要求它在金属、聚合物、陶瓷、复合材料、弹性体或木材之间进行选择。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543069%2F11_-_002_-_Parallelization_Workflows_02.1748543069350.jpg)虽然这种方法可能有效，但你是在要求 Claude 在单个请求中承担大量繁重工作。没有针对每种材料类型的具体标准，结果不会像它们应该的那样可靠。

你可能会想通过在一个巨大的提示词中为每种材料添加详细标准来改进这一点。但这会产生一个新问题——Claude 必须同时处理所有这些不同的考虑因素，这可能导致混乱和次优结果。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543069%2F11_-_002_-_Parallelization_Workflows_06.1748543069782.jpg)

## 更好的方法：并行化

与其将所有内容塞进一个请求中，你可以将任务拆分为多个并行请求。每个请求专注于使用专门的标准评估零件对单一材料类型的适用性。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543070%2F11_-_002_-_Parallelization_Workflows_09.1748543070332.jpg)它的工作原理如下：

* 同时多次向 Claude 发送相同的图像
* 每个请求包含针对一种材料的专门标准（金属标准、聚合物标准、陶瓷标准等）
* Claude 独立评估零件对每种材料的适用性
* 收集所有分析结果并将它们输入最终的聚合步骤

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543070%2F11_-_002_-_Parallelization_Workflows_11.1748543070706.jpg)最后一步将所有单独的分析结果发送回 Claude，请求比较它们并给出最终的材料推荐。

## 并行化 Workflow 的运作方式

并行化模式遵循一个简单的结构：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543071%2F11_-_002_-_Parallelization_Workflows_15.1748543071284.jpg)* **将单个任务拆分为多个子任务** - 将复杂的决策分解为专注的、专门化的评估

* **并行运行子任务** - 同时执行所有评估以加快处理速度
* **将结果聚合在一起** - 将专门的分析合并为最终决策
* **并行化的子任务不需要完全相同** - 每个子任务可以有专门的提示词、Tool 集或评估标准

## 这种方法的优势

并行化 Workflow 提供了几个关键优势：

**专注的注意力：** Claude 可以一次专注于一个特定方面，而不是试图同时平衡多个相互竞争的考虑因素。这导致对每种材料类型的分析更加彻底和准确。

**更容易优化：** 你可以独立改进和测试每种材料评估的提示词。如果你的金属分析效果不好，你可以只改进那个提示词而不影响其他的。

**更好的可扩展性：** 添加新材料进行评估很简单——只需添加另一个并行请求。你不需要重写现有的提示词或担心新标准可能如何干扰现有的标准。

**提高可靠性：** 通过分解复杂任务，你减少了 AI 模型的认知负担，获得更一致、更可靠的结果。

## 何时使用并行化

当你有一个可以分解为独立评估的复杂决策时，这种模式效果很好。寻找那些你要求 AI 考虑多个标准、比较多个选项或做出涉及不同专业领域决策的情况。

关键是识别可以有意义地分离的任务——每个并行子任务应该能够独立运行，并为最终决策贡献独特的分析部分。

# 链式 Workflow

链式 Workflow 乍看起来可能很显而易见，但它们实际上是你在使用 Claude 时会遇到的最有用的模式之一。当你处理复杂任务或 Claude 难以一致处理的长提示词时，这种方法变得特别有价值。

## 什么是 Workflow 链

链式 Workflow 将一个大型复杂任务分解为更小的、顺序执行的子任务。与其要求 Claude 一次完成所有事情，你将工作拆分为相互依赖的专注步骤。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543144%2F11_-_003_-_Chaining_Workflows_03.1748543144730.jpg)这里有一个实际的例子：假设你正在构建一个社交媒体营销工具，可以自动创建和发布视频。与其要求 Claude 在一个巨大的提示词中处理所有事情，你可以将其分解如下：

* 在 Twitter 上查找相关的热门话题
* 选择最有趣的话题（使用 Claude）
* 研究该话题（使用 Claude）
* 为短视频编写脚本（使用 Claude）
* 使用 AI 头像和文本转语音创建视频
* 将视频发布到社交媒体

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543145%2F11_-_003_-_Chaining_Workflows_08.1748543145309.jpg)

## 为什么要链式而不是一个大提示词？

你可能会想为什么不直接将所有 Claude 任务合并到一个提示词中。关键的好处是专注——当你一次给 Claude 一个特定任务时，它可以专注于把那个任务做好，而不是同时应付多个需求。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543145%2F11_-_003_-_Chaining_Workflows_09.1748543145813.jpg)链式方法提供了几个优势：

* 将大任务拆分为更小的、不可并行化的子任务
* 可选择在每个任务之间进行非 LLM 处理
* 让 Claude 专注于整体任务的一个方面

## 长提示词问题

这就是链式真正变得有价值的地方。你经常会遇到需要 Claude 编写具有许多特定约束的内容的情况。假设你想让 Claude 写一篇技术文章，并指定它应该：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543146%2F11_-_003_-_Chaining_Workflows_11.1748543146214.jpg)* 不提及它是由 AI 编写的

* 避免使用表情符号
* 跳过陈词滥调或过于随意的语言
* 以专业、技术性的语气写作

即使所有这些约束都清楚地陈述了，Claude 可能仍然会生成违反某些规则的内容。你可能会收到一篇仍然使用表情符号、提到 AI 作者身份或听起来不专业的文章。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543146%2F11_-_003_-_Chaining_Workflows_13.1748543146542.jpg)

## 链式解决方案

与其与一个巨大的提示词作斗争，使用两步链式方法：

**步骤 1：** 发送你的初始提示词，并接受第一个结果可能不完美。Claude 会生成一篇文章，但它可能违反你的一些约束。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543147%2F11_-_003_-_Chaining_Workflows_14.1748543146936.jpg)**步骤 2：** 发出专门针对修复问题的后续请求。提供 Claude 刚刚写的文章，并给它有针对性的修改指令：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543148%2F11_-_003_-_Chaining_Workflows_17.1748543148012.jpg)

`修改下面提供的文章。按照以下步骤重写文章：`

`1. 识别文本中任何标明作者是 AI 的位置并删除它们 `

`2. 查找并删除所有表情符号 `

`3. 定位任何令人尴尬的写作并用技术写作者会写的文本替换`

这种方法有效是因为 Claude 可以完全专注于修改任务，而不是试图在内容创建和约束遵守之间取得平衡。

## 何时使用链式

链式 Workflow 在以下情况下特别有用：

* 你有具有多个需求的复杂任务
* Claude 在长提示词中持续忽略某些约束
* 你需要在步骤之间处理或验证输出
* 你希望保持每次交互的专注和可管理性

虽然链式可能看起来像是额外的工作，但它通常比试图将所有内容塞进一个提示词产生更好的结果。关键是认识到任务何时足够复杂，值得被分解为专注的、顺序的步骤。

# 路由 Workflow

路由 Workflow 解决了 AI 应用中的一个常见问题：不同类型的用户请求需要不同的处理方式。与其使用一刀切的提示词，你可以对传入的请求进行分类，并将它们路由到专门的处理管道。

## 通用提示词的问题

考虑一个根据用户话题生成视频脚本的社交媒体营销工具。用户可能输入"编程"或"冲浪"作为他们的话题，但这些应该产生非常不同类型的内容：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543142%2F11_-_004_-_Routing_Workflows_02.1748543142365.jpg)编程话题需要具有清晰解释和定义的教育内容。冲浪话题则更适合强调刺激和视觉吸引力的娱乐性脚本。单一的通用提示词无法有效处理两者。

## 设置内容分类

第一步是定义你的应用可能需要生成的不同类型内容。你可以将请求分类为以下类型：

* 娱乐 - 高能量、文化相关的内容，使用流行语言
* 教育 - 清晰、引人入胜的解释，配有易于理解的示例
* 喜剧 - 犀利、出人意料的内容，具有巧妙的观察和时机
* 个人 vlog - 真实、亲密的内容，采用对话式叙事
* 评测 - 果断、基于体验的内容，突出优缺点
* 讲故事 - 沉浸式内容，使用生动的细节和情感连接

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543143%2F11_-_004_-_Routing_Workflows_07.1748543143540.jpg)每个类别都有自己专门的提示词模板。例如，教育提示词可能要求 Claude"开发一个清晰、引人入胜的脚本，将复杂信息转化为易于理解的见解，使用易于理解的示例和发人深省的问题。"

## 路由在实践中如何运作

路由过程分两步进行：

1. **分类** - 将用户的话题发送给 Claude，请求将其分类到你预定义的类型之一
2. **专门处理** - 使用分类结果选择适当的提示词模板并生成内容

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543144%2F11_-_004_-_Routing_Workflows_13.1748543144107.jpg)例如，如果用户输入"Python 函数"作为他们的话题，你首先要求 Claude 对其进行分类：

```
将视频的话题分类到列出的类别之一：
<topic>Python 函数</topic>

<categories>
- 教育
- 娱乐
- 喜剧
- 个人 vlog
- 评测
- 讲故事
</categories>
```

Claude 回复"教育"，所以你然后使用教育提示词模板来生成实际的脚本内容。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543145%2F11_-_004_-_Routing_Workflows_15.1748543144938.jpg)

## 路由 Workflow 架构

路由 Workflow 遵循以下模式：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543145%2F11_-_004_-_Routing_Workflows_17.1748543145286.jpg)* 用户输入首先进入路由组件

* 路由器使用初始的 Claude 调用对请求进行分类
* 根据类别，输入被转发到一个特定的处理管道
* 每个管道可以有自己的 Workflow、提示词或针对该类别优化的 Tool

关键见解是用户输入只进入一个专门的管道，而不是全部。这允许每个管道针对其特定用例进行高度优化。

## 何时使用路由

路由 Workflow 在以下情况下效果很好：

* 你的应用处理需要不同方法的多样化请求类型
* 你可以清楚地定义涵盖你用例的类别
* 分类步骤可以由 Claude 可靠地处理
* 专门处理的性能优势超过了路由步骤的开销

这种模式对于客服机器人、内容生成工具以及任何"正确"响应在很大程度上取决于理解请求类型的应用特别有价值。

# Agent 与 Tool

Agent 代表了与我们一直在研究的结构化 Workflow 的转变。虽然当你知道完成任务所需的确切步骤时，Workflow 是完美的，但当你不确定这些步骤应该是什么时，Agent 就会大放异彩。与其定义一个严格的序列，你给 Claude 一个目标和一组 Tool，然后让它自己决定如何组合这些 Tool 来实现目标。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543186%2F11_-_005_-_Agents_and_Tools_00.1748543186504.jpg)这种灵活性使 Agent 对于构建需要处理各种不可预测任务的应用具有吸引力。你可以创建一个 Agent，确保它工作得相当好，然后部署它来解决各种各样的问题。然而，这种灵活性在可靠性和成本方面是有代价的，我们稍后会探讨。

## Tool 如何构成 Agent

Agent 的真正力量在于它们以意想不到的方式组合简单 Tool 的能力。考虑一组基本的日期时间 Tool：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543187%2F11_-_005_-_Agents_and_Tools_04.1748543186919.jpg)* `get_current_datetime` - 获取当前日期和时间

* `add_duration_to_datetime` - 向给定日期添加时间
* `set_reminder` - 为特定时间创建提醒

这些 Tool 单独看起来很简单，但 Claude 可以将它们链接在一起来处理令人惊讶的复杂请求：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543187%2F11_-_005_-_Agents_and_Tools_05.1748543187417.jpg)对于"现在几点？"，Claude 只需调用 `get_current_datetime`。但对于"11 天后是星期几？"，它会链接 `get_current_datetime` 然后是 `add_duration_to_datetime`。对于设置下周三的健身房提醒，它可能会按顺序使用所有三个 Tool。

Claude 甚至可以识别何时需要更多信息。如果你问"我的 90 天保修什么时候到期？"，它知道在计算到期日期之前要询问你何时购买的物品。

## Tool 应该是抽象的

构建有效 Agent 的关键见解是提供合理抽象的 Tool，而不是超级专门化的 Tool。Claude  Code 完美地展示了这一原则。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543188%2F11_-_005_-_Agents_and_Tools_11.1748543187917.jpg)Claude  Code 可以访问通用的、灵活的 Tool，如：

* `bash` - 运行任何命令
* `read` - 读取任何文件
* `write` - 创建任何文件
* `edit` - 修改文件
* `glob` - 查找文件
* `grep` - 搜索文件内容

值得注意的是，它没有像"重构代码"或"安装依赖"这样的专门 Tool。相反，Claude 自己决定如何使用基本 Tool 来完成这些复杂任务。这种抽象使它能够处理开发人员从未明确计划的无数编程场景。

## 最佳实践：可组合的 Tool

在设计 Agent 时，提供 Claude 可以创造性组合的 Tool。例如，一个社交媒体视频 Agent 可能包括：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543188%2F11_-_005_-_Agents_and_Tools_16.1748543188372.jpg)* `bash` - 访问 FFMPEG 进行视频处理

* `generate_image` - 根据提示词创建图像
* `text_to_speech` - 将文本转换为音频
* `post_media` - 将内容上传到社交平台

这个 Tool 集支持简单的 Workflow（创建和发布视频）和更具交互性的体验，Agent 可能会先生成示例图像，获得用户批准，然后继续视频创建。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543188%2F11_-_005_-_Agents_and_Tools_19.1748543188734.jpg)Agent 可以根据用户反馈和偏好调整其方法，这是使用严格 Workflow 难以实现的。这种灵活性正是 Agent 在构建动态、响应用户的应用方面强大的原因。

# 环境检查

在构建 AI Agent 时，一个关键概念经常被忽视：环境检查。Claude 是盲目运作的——它需要能够观察和理解其行动的结果才能有效工作。

## 为什么环境检查很重要

想想 Claude 如何与计算机使用功能配合工作。每次 Claude 执行一个动作，如输入文本或点击按钮，它都会立即收到一张截图来了解发生了什么。这不仅仅是一个锦上添花的功能——它是必不可少的。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543181%2F11_-_006_-_Environment_Inspection_00.1748543181585.jpg)从 Claude 的角度来看，点击一个按钮可能会导航到一个新页面、打开一个菜单，或触发任何数量的变化。如果不能看到结果，Claude 就无法了解其行动是否成功或环境的新状态是什么样子。

## 先读后写

同样的原则也适用于文件操作。在 Claude 修改任何文件之前，它需要了解当前的内容。这可能看起来很显而易见，但这是你在构建 Agent 时应该始终遵循的模式。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543182%2F11_-_006_-_Environment_Inspection_08.1748543182126.jpg)在上面的例子中，当被要求向 Python 文件添加新路由时，Claude 首先读取现有代码以了解当前结构。只有这样它才能安全地进行请求的更改而不破坏现有功能。

## 系统提示词中的环境检查

你可以通过系统提示词引导 Claude 检查其环境。对于像视频生成这样的复杂任务，这变得尤为重要。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543182%2F11_-_006_-_Environment_Inspection_11.1748543182591.jpg)考虑一个需要以下功能的视频创建 Agent：

* 使用 FFmpeg 等 Tool 生成视频内容
* 验证音频对话的放置是否正确
* 检查视觉元素是否按预期显示

你可能会包含如下系统提示词指令：

* 使用 bash Tool 运行 whisper.cpp 并生成带时间戳的字幕文件以验证对话放置
* 使用 FFmpeg 定期从视频中提取截图以视觉检查输出
* 将生成的内容与原始要求进行比较

## 环境检查的优势

当 Claude 可以检查其环境时，几个方面会得到改善：

* **更好的进度跟踪** - Claude 可以判断它离完成任务有多近
* **错误处理** - 可以检测和纠正意外结果
* **质量保证** - 可以在认为任务完成之前验证输出
* **自适应行为** - Claude 可以根据观察到的情况调整其方法

## 实践实现

在设计自己的 Agent 时，始终问自己："Claude 如何知道这个行动是否成功？"无论你是在处理文件、API 还是用户界面，都要提供让 Claude 观察其行动结果的 Tool 和指令。

这可能意味着：

* 在修改前读取文件内容
* 在 UI 交互后截取屏幕截图
* 检查 API 响应中的预期数据
* 根据要求验证生成的内容

环境检查将 Claude 从一个盲目执行命令的执行者转变为一个能够真正理解和适应其工作环境的 Agent。

# Workflow vs Agent

在构建 AI 驱动的应用时，你经常需要在两种不同的架构方法之间做出选择：Workflow 和 Agent。每种方法都有明显的优势和权衡，使它们适用于不同的场景。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543217%2F11_-_007_-_Workflows_vs_Agents_00.1748543217764.jpg)## 什么是 Workflow？

Workflow 是一系列预定义的 Claude 调用，旨在解决已知问题或一组问题。当你可以提前想象出步骤流程时使用 Workflow——本质上是当你知道完成任务所需的确切序列时。

把 Workflow 想象成将一个大任务分解为更小、更具体的子任务。每个步骤专注于一个单一领域，这使 Claude 能够更精确地工作。

## 什么是 Agent？

对于 Agent，Claude 获得一组基本 Tool，并被期望制定计划来使用这些 Tool 完成任务。与 Workflow 不同，你不知道将提供什么确切的任务，因此系统需要更具适应性。

Agent 可以通过以意想不到的方式组合 Tool 来创造性地解决各种各样的挑战。

## Workflow 的优势

* Claude 可以一次专注于一个子任务，通常会带来更高的准确性
* 更容易评估和测试，因为你知道每个确切的步骤
* 更可预测和可靠的执行
* 更适合解决特定的、明确定义的问题

## Agent 的优势

* 允许更灵活的用户体验
* 任务完成更加灵活——Claude 可以以意想不到的方式组合 Tool 来完成各种各样的任务
* 可以处理开发过程中未预料到的新情况
* 可以在需要时向用户询问额外输入

## Workflow 的缺点

* 灵活性较差——专门用于解决特定类型的任务
* 通常用户体验更受限——你需要知道流程的确切输入
* 需要更多的前期规划和设计工作

## Agent 的缺点

* 与 Workflow 相比，成功任务完成率较低
* 更难进行检测、测试和评估，因为你通常不知道 Agent 会执行什么系列的步骤
* 行为不太可预测

## 何时使用每种方法

作为工程师，你的主要目标是可靠地解决问题。用户可能并不在乎你构建了一个花哨的 Agent——他们想要一个始终如一地工作的产品。

一般建议是尽可能专注于实现 Workflow，只有在真正需要时才使用 Agent。Workflow 提供了大多数生产应用所需的可靠性和可预测性，而 Agent 为那些无法预先确定确切需求的场景提供了灵活性。

当你有明确定义的流程时考虑使用 Workflow，当你需要处理需要创造性问题解决的不可预测、多样化的用户请求时使用 Agent。
