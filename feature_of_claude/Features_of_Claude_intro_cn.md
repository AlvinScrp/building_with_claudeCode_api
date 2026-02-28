# Claude 的功能特性

# 扩展思考

扩展思考是 Claude 的高级推理功能，它让模型在生成最终回复之前有时间深入思考复杂问题。可以把它想象成 Claude 的"草稿纸"——你可以看到得出答案的推理过程，这有助于提高透明度，并且通常能带来更高质量的回复。

## 扩展思考的工作原理

启用扩展思考后，Claude 的回复会从简单的文本块变为包含两部分的结构化响应：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542429%2F08_-_001_-_Extended_Thinking_04.1748542429342.jpg)

启用思考功能后，你会同时获得推理过程和最终答案：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542429%2F08_-_001_-_Extended_Thinking_05.1748542429732.jpg)

主要优势包括：

* 复杂任务的推理能力更强
* 困难问题的准确率更高
* 能够透明地了解 Claude 的思考过程

但也有重要的权衡因素：

* 成本更高（你需要为思考 token 付费）
* 延迟增加（思考需要时间）
* 代码中的响应处理更复杂

## 何时使用扩展思考

决策很简单：使用你的提示词评估结果来判断。先在不启用思考的情况下运行你的提示词，如果在优化提示词之后准确率仍然不满足要求，那么可以考虑启用扩展思考。它是当标准提示词方法还不够好时的一个工具。

## 响应结构与安全性

扩展思考的响应包含一个特殊的签名系统以确保安全：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542430%2F08_-_001_-_Extended_Thinking_06.1748542430208.jpg)

签名是一个加密令牌，确保你没有修改思考文本。这可以防止开发者篡改 Claude 的推理过程，因为篡改可能导致模型产生不安全的行为。

## 编辑后的思考内容

有时你会收到编辑后的思考块，而不是可读的推理文本：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542430%2F08_-_001_-_Extended_Thinking_08.1748542430775.jpg)

这种情况发生在 Claude 的思考过程被内部安全系统标记时。编辑后的内容包含加密形式的实际思考内容，允许你将完整消息传回给 Claude 以便在后续对话中使用，而不会丢失上下文。

## 实现方式

要在代码中启用扩展思考，你需要在聊天函数中添加两个参数：

```
def chat(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,
    thinking_budget=1024
):
```

思考预算设置 Claude 可用于推理的最大 token 数。最小值为 1024 个 token，你的 `max_tokens` 参数必须大于思考预算。

将思考配置添加到你的 API 参数中：

```
if thinking:
    params["thinking"] = {
        "type": "enabled",
        "budget": thinking_budget
    }
```

然后启用思考来调用：

```
chat(messages, thinking=True)
```

## 测试编辑后的响应

出于测试目的，你可以发送一个特殊的触发字符串来强制 Claude 返回编辑后的思考块。这有助于确保你的应用程序能够优雅地处理编辑后的响应而不会崩溃。

扩展思考在你需要 Claude 处理复杂推理任务时是一个强大的功能，但考虑到成本和延迟的影响，请谨慎使用。先从标准提示词开始，充分优化后，当你需要额外的推理能力时再添加思考功能。

请求报文：

```json

{

"max_tokens": 4000,

"messages": [

    {

"role": "user",

"content": "3x+5=14?,求x"

    }

  ],

"model": "claude-opus-4-5-thinking",

"stop_sequences": [],

"temperature": 1,

"thinking": {

"type": "enabled",

"budget_tokens": 1024

  }

}

```

响应报文

```json

{

"id": "req_vrtx_011CY9MQPG2vqZ5Eip8HbXRJ",

"type": "message",

"role": "assistant",

"model": "claude-opus-4-6-thinking",

"content": [

    {

"type": "thinking",

"thinking": "Simple algebra problem.\n\n3x + 5 = 14\n3x = 9\nx = 3"

    },

    {

"type": "text",

"text": "## 求解方程 3x + 5 = 14\n\n**步骤：**\n\n1. **两边减去 5：**\n   $$3x + 5 - 5 = 14 - 5$$\n   $$3x = 9$$\n\n2. **两边除以 3：**\n   $$x = \\frac{9}{3}$$\n\n$$\\boxed{x = 3}$$\n\n**验证：** 3 × **3** + 5 = 9 + 5 = 14 ✅"

    }

  ],

"stop_reason": "end_turn",

"usage": {

"input_tokens": 149,

"output_tokens": 174,

"cache_read_input_tokens": 0,

"cache_creation_input_tokens": 0

  }

}

```

---

# 图像支持

Claude 的视觉能力让你可以在消息中包含图像，并要求 Claude 以各种方式分析它们。你可以要求 Claude 描述图像内容、比较多张图像、计算对象数量，或执行复杂的视觉分析任务。

## 图像处理基础

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542455%2F08_-_002_-_Image_Support_01.1748542455758.jpg)使用图像时需要注意以下重要限制：

* 单个请求中所有消息最多包含 100 张图像
* 每张图像最大 5MB
* 发送单张图像时：最大高度/宽度为 8000px
* 发送多张图像时：最大高度/宽度为 2000px
* 图像可以通过 base64 编码或图像 URL 方式包含
* 每张图像根据其尺寸计算 token 数：`tokens = (宽度 px × 高度 px) / 750`

要向 Claude 发送图像，你需要在用户消息中包含一个图像块和文本块。结构如下：

```
with open("image.png", "rb") as f:
    image_bytes = base64.standard_b64encode(f.read()).decode("utf-8")

add_user_message(messages, [
    # 图像块
    {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": image_bytes,
        }
    },
    # 文本块
    {
        "type": "text",
        "text": "What do you see in this image?"
    }
])
```

## 消息流程

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542456%2F08_-_002_-_Image_Support_02.1748542456229.jpg)对话的工作方式与纯文本交互完全相同。你的服务器发送一条包含图像块和文本块的用户消息给 Claude，Claude 以包含分析结果的文本块作为回复。

## 提示词技巧

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542457%2F08_-_002_-_Image_Support_04.1748542456885.jpg)获得好结果的关键是应用与文本相同的提示词工程技巧。简单的提示词往往会导致差的结果。例如，问"这张图片中有多少颗弹珠？"可能会返回不正确的计数。

你可以通过以下方式显著提高 Claude 的准确率：

* 提供详细的指导方针和分析步骤
* 使用单样本或多样本示例
* 将复杂任务分解为更小的步骤

### 逐步分析

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542457%2F08_-_002_-_Image_Support_05.1748542457338.jpg)与其问一个简单的问题，不如为 Claude 提供一套方法论：

> 分析这张弹珠图片，并使用以下方法确定准确数量：
>
> 1. 首先逐个识别每颗独特的弹珠。在识别时为每颗弹珠分配一个编号。
> 2. 通过不同的方法验证你的结果。从左下角开始，从左到右逐行计数。
>
> 这张图片中弹珠的准确验证数量是多少？

### 单样本示例

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542458%2F08_-_002_-_Image_Support_07.1748542457815.jpg)你还可以通过在消息中提供示例来提高准确率。包含一张已知数量的图像，说明正确答案，然后询问你的目标图像。这为 Claude 提供了你想要的分析类型的参考点。

## 实际案例：火灾风险评估

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542458%2F08_-_002_-_Image_Support_08.1748542458276.jpg)这是一个实际应用：为房屋保险自动化火灾风险评估。保险公司可以使用卫星图像和 Claude 的分析能力，而不是派检查员到每处房产。

该系统分析卫星图像以识别：

* 住宅附近密集、紧凑的树木
* 紧急服务难以到达的通道
* 悬挂在住宅上方的树枝

与其用简单的提示词如"提供一个火灾风险评分"，一个结构良好的提示词会将分析分解为具体步骤：

请按以下步骤分析附件中的房产卫星图像：

1. 住宅识别：定位房产中的主要住宅，查找：

* 最大的有屋顶结构
* 典型住宅特征（车道连接、规则几何形状）
* 与其他结构的区别（车库、棚屋、游泳池）

  2.树冠悬垂分析：检查主要住宅附近的所有树木：
* 识别树冠直接悬垂在屋顶任何部分的树木
* 估算被悬垂树枝覆盖的屋顶百分比（0-25%、25-50%、50-75%、75%+）
* 注意特别密集的悬垂区域

3.火灾风险评估：对于任何悬垂的树木，评估：

* 潜在的野火脆弱性（余烬捕获点、通向结构的连续燃料路径）
* 与烟囱、通风口或其他可见屋顶开口的接近程度
* 树枝在野外植被与结构之间形成“桥梁”的区域

4.防御空间识别：评估房产的整体植被结构：

* 识别树木是否连接形成覆盖或靠近房屋的连续树冠
* 注意任何明显的燃料阶梯（可将火势从地面带到树木再到屋顶的植被）

5.火灾风险评级：根据分析，给出 1-4 级的火灾风险评级：

* 评级 1（低风险）：没有树枝悬垂在屋顶上，房屋周围有良好的防御空间
* 评级 2（中等风险）：最小悬垂（<25% 屋顶），树冠之间有一定分离
* 评级 3（高风险）：显著悬垂（25-50% 屋顶），连接的树冠，多个脆弱点
* 评级 4（严重风险）：广泛悬垂（>50% 屋顶），结构附近密集植被

对于上述每项（1-5），请用一句话总结你的发现，最终回答为数字评级。

这个详细的提示词引导 Claude 进行系统化分析，比简单的请求能产生更准确、更有用的评估结果。

记住：适用于文本的提示词技巧同样适用于图像。如果你想要可靠的结果，请花时间构建详细、结构化的提示词，而不是依赖简单的问题。

# PDF 支持

Claude 可以直接读取和分析 PDF 文件，使其成为文档处理的强大工具。此功能的工作方式与图像处理类似，但在代码结构上有一些关键区别。

## 设置 PDF 处理

使用 Claude 处理 PDF 文件的代码与处理图像的代码几乎相同。主要区别在于文件类型规范和为清晰起见的变量名称。

以下是如何将现有的图像处理代码修改为处理 PDF：

```
with open("earth.pdf", "rb") as f:
    file_bytes = base64.standard_b64encode(f.read()).decode("utf-8")

messages = []

add_user_message(
    messages,
    [
        {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": file_bytes,
            },
        },
        {"type": "text", "text": "Summarize the document in one sentence"},
    ],
)

chat(messages)
```

## 与图像处理的主要区别

将图像处理代码改编为 PDF 时，你需要更新以下几个元素：

* 将文件扩展名从 `.png` 改为 `.pdf`
* 为了清晰起见，将变量名从 `image_bytes` 更新为 `file_bytes`
* 将类型设置为 `"document"` 而非 `"image"`
* 将媒体类型更改为 `"application/pdf"` 而非 `"image/png"`

## Claude 可以从 PDF 中提取的内容

Claude 的 PDF 处理能力不仅仅是简单的文本提取。它可以分析和理解：

* 文档中的全部文本内容
* PDF 中嵌入的图像和图表
* 表格及其数据关系
* 文档结构和格式

这使得 Claude 实际上成为从 PDF 文档中提取任何类型信息的一站式解决方案，无论你需要摘要、数据分析还是特定内容提取。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542484%2F08_-_003_-_PDF_Support_02.1748542484779.jpg)上面的示例展示了 Claude 成功处理了一篇保存为 PDF 的关于地球的维基百科文章，演示了它如何用一句话理解和总结复杂的文档内容。

# 引用功能

当 Claude 根据你提供的文档回答问题时，用户可能会认为它只是从训练数据中提取信息。但如果 Claude 能够准确显示它从哪里找到了特定信息呢？这就是引用功能的作用——一项强大的功能，让 Claude 能够引用源文档中的特定部分，并向用户准确展示每条信息的来源。

## 为什么引用功能很重要

想象一下，你问 Claude 关于地球大气层是如何形成的，然后得到了一个详细的答案。如果没有引用，用户无法验证信息或了解 Claude 实际上是在引用你提供的特定文档。引用功能通过创建从 Claude 的回复到源材料的清晰追溯路径来解决这个透明度问题。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542499%2F08_-_004_-_Citations_00.1748542499688.jpg)

## 启用引用功能

要启用引用功能，你需要修改文档消息结构。在文档块中添加两个新字段：

```
{
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": file_bytes,
    },
    "title": "earth.pdf",
    "citations": { "enabled": True }
}
```

`title` 字段为你的文档提供一个可读的名称，而 `citations: {"enabled": True}` 告诉 Claude 追踪信息来源。

## 理解引用结构

启用引用后，Claude 的回复会变得更复杂。你得到的不是简单的文本，而是包含每个声明的引用信息的结构化数据。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542500%2F08_-_004_-_Citations_08.1748542500257.jpg)每个引用包含几个关键信息：

* **cited_text** - 文档中支持 Claude 陈述的确切文本
* **document_index** - Claude 引用的是哪个文档（当你提供多个文档时很有用）
* **document_title** - 你为文档指定的标题
* **start_page_number** - 引用文本的起始位置
* **end_page_number** - 引用文本的结束位置

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542500%2F08_-_004_-_Citations_09.1748542500755.jpg)

## 使用引用构建用户界面

引用的真正力量在于构建让用户能够访问这些信息的用户界面。你可以创建交互式元素，让用户将鼠标悬停在引用标记上以查看信息的确切来源。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542501%2F08_-_004_-_Citations_11.1748542501163.jpg)这创造了一种透明的体验，用户可以：

* 看到 Claude 的回答建立在实际源材料之上
* 通过查看原始文档验证信息
* 了解每条引用信息的上下文

## 纯文本引用

引用功能不限于 PDF 文档。你也可以将其用于纯文本来源。使用文本时，按如下方式修改文档结构：

```
{
    "type": "document",
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": article_text,
    },
    "title": "earth_article",
    "citations": { "enabled": True }
}
```

使用纯文本来源时，你将获得字符位置而不是页码，精确定位 Claude 在文本中找到每条信息的位置。

## 何时使用引用功能

引用功能在以下情况下特别有价值：

* 用户需要验证信息的准确性
* 你正在处理用户应该能够参考的权威文档
* 信息来源的透明度对你的应用程序至关重要
* 用户可能想要探索特定事实的更广泛上下文

通过实现引用功能，你将 Claude 从一个提供答案的"黑箱"转变为一个展示工作过程的透明研究助手。这建立了用户信任，并使他们能够在需要时深入了解你的源材料。

# 提示词缓存

提示词缓存是一项通过重用先前请求的计算工作来加快 Claude 响应速度并降低文本生成成本的功能。Claude 不再在每次请求后丢弃所有处理工作，而是可以在你再次发送类似内容时保存并重用它。

## Claude 通常如何处理请求

要理解提示词缓存，让我们先看看在未启用缓存时典型请求的处理过程。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542537%2F08_-_005_-_Prompt_Caching_01.1748542536808.jpg)当你向 Claude 发送消息时，它不会立即开始生成回复。相反，Claude 会对你的输入进行大量预处理工作：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542537%2F08_-_005_-_Prompt_Caching_04.1748542537345.jpg)* 将提示词分词为更小的片段

* 为每个 token 创建嵌入向量
* 根据周围文本添加上下文
* 然后才生成实际的输出文本

发送回复后，Claude 会丢弃所有这些计算工作——分词、嵌入向量和上下文分析全部被丢弃。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542537%2F08_-_005_-_Prompt_Caching_07.1748542537838.jpg)

## 丢弃工作的问题

当你发出包含相同内容的后续请求时，这就变得低效了。例如，在一个对话中你要求 Claude 对同一段长文本进行摘要优化：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542538%2F08_-_005_-_Prompt_Caching_09.1748542538396.jpg)Claude 不得不对刚刚分析过的内容重复所有相同的预处理工作。正如 Claude 可能会想的那样："我刚刚处理了那条消息并丢弃了所有工作——我本可以重用它的！"

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542539%2F08_-_005_-_Prompt_Caching_11.1748542538911.jpg)

## 提示词缓存如何解决这个问题

提示词缓存通过保存预处理工作而不是丢弃它来改变这个工作流程：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542539%2F08_-_005_-_Prompt_Caching_15.1748542539641.jpg)当你发出初始请求时，Claude 执行所有常规的预处理，但将结果存储在缓存中而不是丢弃。缓存就像一个查找表，表示"如果我再次看到这条消息，我将重用我已经完成的工作。"

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542540%2F08_-_005_-_Prompt_Caching_17.1748542540035.jpg)

## 主要优势和限制

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542540%2F08_-_005_-_Prompt_Caching_19.1748542540458.jpg)提示词缓存提供了以下优势：

* **更快的响应：** 使用缓存内容的请求执行更快
* **更低的成本：** 请求中缓存部分的费用更低
* **自动优化：** 初始请求写入缓存，后续请求从缓存读取

但需要注意以下重要限制：

* **缓存持续时间：** 缓存内容仅保留一小时
* **有限的使用场景：** 仅在你重复发送相同内容时有益
* **高频率要求：** 当相同内容在你的请求中极其频繁地出现时最有效

提示词缓存最适合的场景，如文档分析工作流（你对同一份长文档提出多个问题），或迭代编辑任务（基础内容保持不变，你只优化特定方面）。

# 提示词缓存的规则

提示词缓存通过存储对消息所做的计算工作来实现，以便在后续请求中重用。这使得后续请求的执行更快、更便宜，但前提是你重复发送相同的内容。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542546%2F08_-_006_-_Rules_of_Prompt_Caching_00.1748542546287.jpg)过程很简单：你的初始请求将处理工作写入缓存，后续请求可以从该缓存读取，而无需重新处理相同的内容。缓存保留一小时，因此此功能仅在你在该时间范围内重复发送相同内容时有用。

## 缓存断点

缓存不会自动启用——你需要手动在消息中的特定块上添加缓存断点。工作方式如下：

* 对消息所做的工作**不会自动缓存**
* 你必须手动在块上添加"缓存断点"
* 断点**之前**的所有工作将被缓存
* 仅当断点（含）之前的内容完全相同时，缓存才会在后续请求中被使用

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542547%2F08_-_006_-_Rules_of_Prompt_Caching_04.1748542546894.jpg)要添加缓存断点，你需要使用文本块的完整格式而非简写格式：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542547%2F08_-_006_-_Rules_of_Prompt_Caching_06.1748542547409.jpg)简写格式没有地方添加缓存控制字段，因此你必须使用展开格式，将 `cache_control` 字段设置为 `{"type": "ephemeral"}`。

## 缓存断点的工作原理

当你在消息中放置缓存断点时，Claude 会缓存直到该断点（含）的所有处理工作。断点之后的内容会正常处理，不会被缓存。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542547%2F08_-_006_-_Rules_of_Prompt_Caching_08.1748542547846.jpg)要使缓存在后续请求中有用，断点之前的内容必须完全相同。即使是添加"please"这样的小改动也会使缓存失效，迫使 Claude 重新处理所有内容。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542548%2F08_-_006_-_Rules_of_Prompt_Caching_10.1748542548220.jpg)

## 跨消息缓存

缓存断点可以跨越多条消息和消息类型。如果你在后面的消息中放置断点，所有之前的消息（用户消息、助手消息等）都将包含在缓存内容中。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542548%2F08_-_006_-_Rules_of_Prompt_Caching_11.1748542548748.jpg)这在你想要缓存到某个点的整个上下文的对话中特别有用。

## 系统提示词和工具

你不仅限于文本块——缓存断点可以添加到：

* 系统提示词
* 工具定义
* 图像块
* 工具使用和工具结果块

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542549%2F08_-_006_-_Rules_of_Prompt_Caching_13.1748542549124.jpg)系统提示词和工具定义是缓存的绝佳候选者，因为它们在请求之间很少改变。这通常是你从提示词缓存中获益最多的地方。

## 缓存顺序

在幕后，Claude 按特定顺序处理请求组件：先是工具，然后是系统提示词，最后是消息。理解这个顺序有助于你有效地放置断点。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542550%2F08_-_006_-_Rules_of_Prompt_Caching_15.1748542549957.jpg)你最多可以添加四个缓存断点。例如，你可以缓存你的工具，然后在对话历史中途添加另一个断点。这让你可以灵活地控制当请求的不同部分发生变化时哪些内容被缓存。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542550%2F08_-_006_-_Rules_of_Prompt_Caching_17.1748542550452.jpg)

## 最小内容长度

缓存有一个最低阈值：内容必须至少 1024 个 token 才能被缓存。这是你尝试缓存的所有消息和块的总和，而不是单个块。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542550%2F08_-_006_-_Rules_of_Prompt_Caching_19.1748542550839.jpg)一条简单的"Hi there!"消息不会达到这个阈值，但如果你将该内容复制 500 次（或确实有一个很长的提示词），它将超过 1024 个 token 并有资格被缓存。

有效使用提示词缓存的关键是识别请求中哪些部分在多次调用中保持一致，并策略性地放置断点以最大化重用，同时最小化缓存失效。

# 提示词缓存实战

提示词缓存是一项强大的优化功能，当你向 Claude 重复发送相同内容时，可以使 API 请求更快、更便宜。让我们探索如何在应用程序中有效地实现它。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542595%2F08_-_007_-_Prompt_Caching_in_Action_19.1748542594923.jpg)

## 提示词缓存的工作原理

启用提示词缓存后，第一个请求将内容写入保留一小时的缓存。后续请求可以从此缓存读取，而无需再次处理相同的内容。当你发送以下内容时，这特别有价值：

* 大型系统提示词（如 6K token 的编码助手提示词）
* 复杂的工具模式（多个工具约 1.7K token）
* 重复的消息内容

关键洞察是，缓存仅在你重复发送相同内容时有帮助——但在许多应用程序中，这种情况极其频繁地发生。

## 设置工具模式缓存

要缓存你的工具模式，你需要在工具列表的最后一个工具上添加缓存控制字段。以下是在不修改原始工具定义的情况下正确执行此操作的方法：

```
if tools:
    tools_clone = tools.copy()
    last_tool = tools_clone[-1].copy()
    last_tool["cache_control"] = {"type": "ephemeral"}
    tools_clone[-1] = last_tool
    params["tools"] = tools_clone
```

这种方法在添加缓存控制字段之前创建了工具列表和最后一个工具模式的副本。虽然你可以直接修改 `tools[-1]["cache_control"]`，但复制的方法可以防止你以后重新排序工具时出现问题。

## 系统提示词缓存

对于系统提示词，你需要将其构造为带有缓存控制的文本块：

```
if system:
    params["system"] = [
        {
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"}
        }
    ]
```

这将你的系统提示词从简单的字符串转换为支持缓存的结构化格式。

## 理解缓存行为

当你启用缓存运行请求时，你会在响应中看到不同的使用模式：

* **第一次请求：** `cache_creation_input_tokens=1772` - Claude 写入缓存
* **后续请求：** `cache_read_input_tokens=1772` - Claude 从缓存读取
* **内容更改：** 出现新的缓存创建 token

缓存极其敏感——即使更改工具或系统提示词中的单个字符也会使该组件的整个缓存失效。

## 缓存顺序和断点

你可以在单个请求中设置多个缓存断点。顺序很重要：

1. 工具（如果提供）
2. 系统提示词（如果提供）
3. 消息

如果你更改了系统提示词但保持相同的工具，你会看到部分缓存读取（工具部分）和缓存写入（新的系统提示词部分）。这种细粒度的缓存意味着你只需为实际更改的部分支付处理费用。

## 实际注意事项

提示词缓存在以下情况下最有效：

* 跨请求的一致工具模式
* 稳定的系统提示词
* 使用类似上下文进行多次请求的应用程序

请记住，缓存仅保留一小时，因此它是为 API 使用频率相对较高的应用程序设计的，而不是用于长期存储。

# 代码执行和 Files API

Anthropic API 提供了两个协同工作效果极佳的强大功能：Files API 和代码执行。虽然它们初看可能是独立的，但将它们结合使用为将复杂任务委托给 Claude 开辟了一些非常有趣的可能性。

## Files API

Files API 提供了一种替代的文件上传处理方式。你可以提前上传文件并在之后引用它们，而不是在消息中直接以 base64 数据编码图像或 PDF。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542605%2F08_-_008_-_Code_Execution_and_the_Files_API_01.1748542605372.jpg)工作方式如下：

* 通过单独的 API 调用将文件（图像、PDF、文本等）上传到 Claude
* 接收包含唯一文件 ID 的文件元数据对象
* 在后续消息中引用该文件 ID，而不是包含原始文件数据

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542606%2F08_-_008_-_Code_Execution_and_the_Files_API_02.1748542606050.jpg)当你想要多次引用同一文件或处理较大文件时，这种方法特别有用，因为在每次请求中包含这些文件会很麻烦。

## 代码执行工具

代码执行是一个服务器端工具，不需要你提供实现。你只需在请求中包含一个预定义的工具模式，Claude 就可以选择在隔离的 Docker 容器中执行 Python 代码。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542607%2F08_-_008_-_Code_Execution_and_the_Files_API_04.1748542607054.jpg)代码执行环境的关键特性：

* 在隔离的 Docker 容器中运行
* 无网络访问（不能进行外部 API 调用）
* Claude 可以在单次对话中多次执行代码
* 结果由 Claude 捕获并解释以生成最终回复

## 结合 Files API 和代码执行

真正的力量来自于将这些功能结合使用。由于 Docker 容器没有网络访问权限，Files API 成为将数据传入和传出执行环境的主要方式。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542607%2F08_-_008_-_Code_Execution_and_the_Files_API_06.1748542607578.jpg)典型的工作流程如下：

1. 使用 Files API 上传你的数据文件（如 CSV）
2. 在消息中包含带有文件 ID 的容器上传块
3. 要求 Claude 分析数据
4. Claude 编写并执行代码来处理你的文件
5. Claude 可以生成你可以下载的输出（如图表）

## 实际示例

让我们看一个使用流媒体服务数据的真实示例。CSV 文件包含用户信息，包括订阅等级、观看习惯以及他们是否流失（取消了订阅）。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542608%2F08_-_008_-_Code_Execution_and_the_Files_API_08.1748542608112.jpg)首先，使用辅助函数上传文件：

```
file_metadata = upload('streaming.csv')
```

然后创建一条包含上传文件和分析请求的消息：

```
messages = []
add_user_message(
    messages,
    [
        {
            "type": "text",
            "text": """进行详细分析以确定客户流失的主要驱动因素。你的最终输出应
  至少包含一张总结分析结果的详细图表。"""
        },
        {"type": "container_upload", "file_id": file_metadata.id},
    ],
)

chat(
    messages,
    tools=[{"type": "code_execution_20250522", "name": "code_execution"}]
)
```

## 理解响应

当 Claude 使用代码执行时，响应包含多种类型的块：

* **文本块** - Claude 的分析和解释
* **服务器工具使用块** - Claude 决定运行的实际代码
* **代码执行工具结果块** - 运行代码的输出

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542608%2F08_-_008_-_Code_Execution_and_the_Files_API_13.1748542608585.jpg)Claude 可能在单次回复中多次执行代码，逐步构建其分析。每个执行周期包含代码及其结果。

## 下载生成的文件

最强大的功能之一是 Claude 能够生成文件（如图表或报告）并使其可供下载。当 Claude 创建可视化内容时，它会存储在容器中，你可以使用 Files API 下载它。

在响应中查找 `type: "code_execution_output"` 的块——这些块包含生成内容的文件 ID：

```
download_file("file_id_from_response")
```

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542609%2F08_-_008_-_Code_Execution_and_the_Files_API_18.1748542609010.jpg)结果是一份综合分析，带有专业的可视化图表，手动编码制作这些将需要大量工作。

## 超越数据分析

虽然数据分析是一个自然的应用场景，但 Files API 和代码执行的结合开辟了许多可能性：

* 图像处理和操作
* 文档解析和转换
* 数学计算和建模
* 自定义格式的报告生成

关键在于你可以将复杂的计算任务委托给 Claude，同时通过 Files API 保持对输入和输出的控制。这创建了一个强大的工作流程，Claude 成为你的编码助手，能够实际执行和迭代解决方案。
