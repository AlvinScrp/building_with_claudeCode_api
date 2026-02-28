# 检索增强生成简介

检索增强生成（RAG）是一种帮助你处理大型文档的技术，这些文档太大而无法放入单个提示中。RAG不是将所有内容塞进一个庞大的提示中，而是将文档分解成块，并在回答问题时只包含最相关的部分。

## 大型文档的问题

想象一下，你有一份800页的财务文档，想向Claude询问有关它的具体问题，比如"这家公司有哪些风险因素？"你需要以某种方式将文档中的相关信息传递给Claude，但提示中可以包含的文本量是有限制的。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542174%2F07_-_001_-_Introducing_Retrieval_Augmented_Generation_01.1748542174442.jpg)

## 选项1：将所有内容包含在提示中

第一种方法很简单——从文档中提取所有文本，并将其与用户的问题一起塞入提示中。你的提示可能如下所示：

```
回答用户关于财务文档的问题。

<user_question>
{user_question}
</user_question>

<financial_document>
{financial_document}
</financial_document>
```

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542175%2F07_-_001_-_Introducing_Retrieval_Augmented_Generation_05.1748542174970.jpg)

这种方法有严重的局限性：

* 提示长度有硬性限制——你的文档可能太长
* Claude在处理非常长的提示时效果会变差
* 更大的提示处理成本更高
* 更大的提示处理时间更长

## 选项2：将文档分解成块

RAG采用了更智能的方法。首先，在预处理步骤中将文档分解成较小的块。然后，当用户提出问题时，找到与其问题最相关的块，并仅将这些块包含在提示中。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542175%2F07_-_001_-_Introducing_Retrieval_Augmented_Generation_08.1748542175384.jpg)

工作原理如下：如果有人问"这家公司面临哪些风险？"你会搜索你的块，找到"风险因素"部分，并仅将该相关块包含在提示中。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542175%2F07_-_001_-_Introducing_Retrieval_Augmented_Generation_09.1748542175794.jpg)

## RAG的优势

* Claude可以只关注最相关的内容
* 可扩展到非常大的文档
* 适用于多个文档
* 更小的提示成本更低且运行更快

## RAG的挑战

* 需要预处理步骤来分块文档
* 需要搜索机制来找到"相关"的块
* 包含的块可能不包含Claude需要的所有上下文
* 有多种分块文本的方法——哪种方法最好？

例如，你可以将文档分成大小相等的部分，或者可以根据文档结构（如标题和章节）创建块。每种方法都有权衡，你需要根据具体用例进行评估。

## 何时使用RAG

RAG涉及许多技术决策，比简单地将所有内容包含在提示中需要更多工作。你需要分析对于你的特定应用，收益是否超过复杂性。当处理非常大的文档、多个文档，或需要优化成本和性能时，它特别有价值。

关键见解是RAG用简单性换取可扩展性和效率。虽然它需要更多的前期工作来正确实现，但它使你能够处理用简单的提示填充无法处理的文档集合。

# 文本分块策略

文本分块是构建RAG（检索增强生成）管道中最关键的步骤之一。你如何分解文档直接影响整个系统的质量。糟糕的分块策略可能导致不相关的上下文被插入到提示中，导致AI给出完全错误的答案。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542228%2F07_-_002_-_Text_Chunking_Strategies_01.1748542228739.jpg)

考虑这个例子：你有一份包含医学研究和软件工程部分的文档。如果分块不当，用户询问"工程师今年修复了多少bug？"可能会得到关于医学研究而不是软件工程的信息，仅仅因为医学部分恰好在不同的上下文中包含了"bug"这个词。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542229%2F07_-_002_-_Text_Chunking_Strategies_04.1748542229353.jpg)

这就是为什么选择正确的分块策略如此重要。让我们探讨三种主要方法。

## 基于大小的分块

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542230%2F07_-_002_-_Text_Chunking_Strategies_05.1748542229862.jpg)

基于大小的分块是最简单的方法——你将文本分成等长的字符串。如果你有一个325个字符的文档，你可能会将其分成三个大约108个字符的块。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542230%2F07_-_002_-_Text_Chunking_Strategies_06.1748542230454.jpg)

这种方法易于实现并适用于任何类型的文档，但它有明显的缺点：

* 单词会在句子中间被截断
* 块会失去周围文本的重要上下文
* 章节标题可能与其内容分离

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542231%2F07_-_002_-_Text_Chunking_Strategies_07.1748542230923.jpg)

为了解决这些问题，你可以在块之间添加重叠。这意味着每个块包含来自相邻块的一些字符，提供更好的上下文并确保完整的单词和句子。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542231%2F07_-_002_-_Text_Chunking_Strategies_08.1748542231502.jpg)

这是一个基本实现：

```
def chunk_by_char(text, chunk_size=150, chunk_overlap=20):
    chunks = []
    start_idx = 0

    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))
        chunk_text = text[start_idx:end_idx]
        chunks.append(chunk_text)

        start_idx = (
            end_idx - chunk_overlap if end_idx < len(text) else len(text)
        )

    return chunks
```

## 基于结构的分块

基于结构的分块根据文档的自然结构（标题、段落和章节）来划分文本。当你有格式良好的文档（如Markdown文件）时，这种方法效果很好。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542232%2F07_-_002_-_Text_Chunking_Strategies_09.1748542232356.jpg)

对于Markdown文档，你可以按标题标记分割：

```
def chunk_by_section(document_text):
    pattern = r"\n## "
    return re.split(pattern, document_text)
```

这种方法为你提供最干净、最有意义的块，因为每个块都代表一个完整的章节。然而，它只在你对文档结构有保证时才有效。许多现实世界的文档是纯文本或PDF，没有清晰的结构标记。

## 基于语义的分块

基于语义的分块是最复杂的方法。你将文本分成句子，然后使用自然语言处理来确定连续句子的相关程度。你从相关句子组构建块。

这种方法计算成本高，但产生最相关的块。它需要理解单个句子的含义，并且比其他策略更复杂。

## 基于句子的分块

一个实用的折中方案是按句子分块。你使用正则表达式将文本分成单个句子，然后将它们分组成块，可选择性地添加重叠：

```
def chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1):
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    start_idx = 0

    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))
        current_chunk = sentences[start_idx:end_idx]
        chunks.append(" ".join(current_chunk))

        start_idx += max_sentences_per_chunk - overlap_sentences

        if start_idx < 0:
            start_idx = 0

    return chunks
```

## 选择你的策略

你的选择完全取决于你的用例和文档保证：

* **基于结构**：当你控制文档格式时效果最好（如内部公司报告）
* **基于句子**：对大多数文本文档来说是很好的折中方案
* **基于大小**：最可靠的后备方案，适用于任何内容类型，包括代码

带重叠的基于大小的分块通常是生产环境中的首选，因为它简单、可靠，并且适用于任何文档类型。虽然它可能不会给出完美的结果，但它始终产生合理的块，不会破坏你的管道。

记住：没有单一的"最佳"分块策略。正确的方法取决于你的具体文档、用例，以及你愿意在实现复杂性和块质量之间做出的权衡。

# 文本嵌入

在将文档分解成块之后，RAG管道的下一步是找到哪些块与用户的问题最相关。这本质上是一个搜索问题——你需要查看所有文本块并识别与用户询问内容相关的块。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542211%2F07_-_003_-_Text_Embeddings_03.1748542211434.jpg)

### 寻找相关文本块 (Finding Relevant Chunks)

* **这是一个搜索问题！**
* **我们如何找到与用户问题最相关的文本块？**

#### 用户的问题 (User's Question)

> **工程师今年修复了多少个 Bug？**

#### 文本块 (Chunks of Text)

为了回答上述问题，系统需要从以下“知识库”中提取信息：

1. **背景介绍：** 今年我们公司参与了多个领域的研究。
2. **## 第 1 节：医学研究**
   今年我们在理解 XDR-47 方面取得了重大进展，这是一种我们以前从未见过的**“bug”**（此处指病原体）。
3. **## 第 2 节：软件工程**
   该部门投入了大量精力研究我们分布式系统中的各种**感染途径** (infection vectors)。

---

#### 核心挑战解析

这张幻灯片向观众提出了一个挑战：**传统的关键词匹配在这里会失效。**

* **陷阱：** 第 1 节中出现了“bug”这个词，但它指的是医学上的病毒，与用户想问的“工程师修复 Bug”完全无关。
* **关联性：** 第 2 节虽然没有出现“bug”这个词，但提到了“软件工程”和“分布式系统”，这才是工程师真正工作的地方。

**语义搜索**的作用就是超越字面意思，利用向量嵌入技术识别出第 2 节才是真正相关的答案来源。

## 语义搜索

找到相关块的最常见方法是语义搜索。与寻找精确单词匹配的基于关键字的搜索不同，语义搜索使用文本嵌入来理解用户问题和每个文本块的含义和上下文。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542212%2F07_-_003_-_Text_Embeddings_04.1748542212115.jpg)

**利用文本嵌入（Text Embeddings）来更好地理解用户的提问，以及每一段文本内容的真正含义。**

这张图巧妙地展示了**语义搜索**的重要性：

* 用户虽然问的是“修复了多少个 Bug”（通常指软件错误）。
* 但在医学研究段落中，“Bug”指的是病毒。
* 在软件工程段落中，虽然没出现“Bug”一词，但提到了“感染途径”。
* **语义搜索**的目标就是区分这些语境，找到真正相关的答案，而不是简单的关键词匹配。

## 文本嵌入

文本嵌入是文本中包含的含义的数值表示。可以将其视为将单词和句子转换为计算机可以进行数学处理的格式。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542212%2F07_-_003_-_Text_Embeddings_07.1748542212576.jpg)

工作流程如下：

* 你将文本输入嵌入模型
* 模型输出一长串数字（嵌入）
* 每个数字的范围从-1到+1
* 这些数字代表输入文本的不同质量或特征

## 理解这些数字

嵌入中的每个数字本质上是输入文本某种质量的"分数"。然而，这里有一个重要的警告：我们不知道每个数字精确代表什么。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542213%2F07_-_003_-_Text_Embeddings_09.1748542213029.jpg)

虽然想象一个数字可能代表"文本有多快乐"或"文本谈论海洋的程度"是有帮助的，但这些只是概念性的例子。每个维度的实际含义是模型在训练期间学习的，人类无法直接解释。

## 使用VoyageAI生成嵌入

由于Anthropic目前不提供嵌入生成，推荐的提供商是VoyageAI。你需要：

* 注册一个单独的VoyageAI账户
* 获取API密钥（免费开始）
* 将密钥添加到你的环境变量中

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542213%2F07_-_003_-_Text_Embeddings_15.1748542213569.jpg)

在你的 `.env`文件中，添加：

```
VOYAGE_API_KEY="your_key_here"
```

## 实现

首先，安装VoyageAI库：

```
%pip install voyageai
```

然后设置客户端并创建一个生成嵌入的函数：

```
from dotenv import load_dotenv
import voyageai

load_dotenv()
client = voyageai.Client()

def generate_embedding(text, model="voyage-3-large", input_type="query"):
    result = client.embed([text], model=model, input_type=input_type)
    return result.embeddings[0]
```

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542214%2F07_-_003_-_Text_Embeddings_18.1748542214005.jpg)

当你在文本块上运行此函数时，你将获得一个表示嵌入的浮点数列表。这个过程快速而直接——真正的挑战是理解如何在RAG管道中有效地使用这些嵌入来找到最相关的内容。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542214%2F07_-_003_-_Text_Embeddings_19.1748542214605.jpg)

下一步是学习如何比较嵌入以确定哪些块与用户的问题最相似，这构成了语义搜索过程的核心。

# 完整的RAG流程

现在我们已经介绍了RAG、文本分块和嵌入的基础知识，让我们逐步了解完整的RAG管道。这个例子将向你展示所有这些部分如何协同工作以检索相关信息并生成响应。

## 步骤1：分块你的源文本

首先，我们获取源文档并将其分解成可管理的块。对于这个例子，我们将使用两个简单的文本部分：

* 第1部分：医学研究 - "今年我们对XDR-47的理解取得了重大进展，这是一个我们以前从未见过的'bug'。"
* 第2部分：软件工程 - "该部门投入了大量精力研究我们分布式系统中的各种感染向量"

## 步骤2：生成嵌入

接下来，我们使用嵌入模型将每个文本块转换为数值嵌入。为了更容易理解，让我们想象我们有一个完美的嵌入模型，它总是返回恰好两个数字，并且我们知道每个数字代表什么。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542285%2F07_-_004_-_The_Full_RAG_Flow_02.1748542285571.jpg)

在我们想象的模型中：

* 第一个数字代表文本谈论医学领域的程度
* 第二个数字代表文本谈论软件工程的程度

对于医学研究部分，我们可能得到 `[0.97, 0.34]` - 非常专注于医学，但由于"bug"一词而带有一些软件元素。对于软件工程部分，我们得到 `[0.30, 0.97]` - 高度专注于软件，但由于"感染向量"而带有医学色彩。

## 归一化

嵌入API通常执行归一化步骤，将每个向量缩放到大小为1.0。你不需要担心这里的数学——它是自动处理的。这给我们归一化的向量，如 `[0.944, 0.331]`和 `[0.295, 0.955]`。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542286%2F07_-_004_-_The_Full_RAG_Flow_07.1748542286054.jpg)

我们可以在单位圆上可视化这些嵌入，其中每个点代表我们的一个文本块。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542287%2F07_-_004_-_The_Full_RAG_Flow_08.1748542287015.jpg)

## 步骤3：存储在向量数据库中

我们将这些嵌入存储在向量数据库中——一个专门优化用于存储、比较和搜索长数字列表（如我们的嵌入）的数据库。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542287%2F07_-_004_-_The_Full_RAG_Flow_09.1748542287378.jpg)

此时，我们暂停。到目前为止的所有工作都是提前进行的预处理。现在我们等待用户提交查询。

## 步骤4：处理用户查询

当用户提出问题，如"我对公司很好奇。特别是，软件工程部门今年做了什么？"时，我们通过相同的嵌入模型运行他们的查询。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542287%2F07_-_004_-_The_Full_RAG_Flow_10.1748542287773.jpg)

这个查询被嵌入为类似 `[0.1, 0.89]`的东西——低医学分数，高软件工程分数。归一化后，我们得到 `[0.112, 0.993]`。

## 步骤5：查找相似的嵌入

我们将用户的查询嵌入发送到向量数据库，并要求它找到最相似的存储嵌入。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542288%2F07_-_004_-_The_Full_RAG_Flow_12.1748542288192.jpg)

数据库返回软件工程部分，因为它与用户询问的内容最匹配。

## 相似度如何工作：余弦相似度

向量数据库使用余弦相似度来确定哪些嵌入最相似。这测量两个向量之间角度的余弦值。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542288%2F07_-_004_-_The_Full_RAG_Flow_15.1748542288516.jpg)

关于余弦相似度的要点：

* 结果范围从-1到1
* 接近1的值表示高相似度
* 接近-1的值表示非常不同
* 0表示垂直（无关系）

在我们的例子中，用户查询和软件工程块之间的余弦相似度是0.983——非常高的相似度。与医学研究块的相似度只有0.398——低得多。

## 余弦距离

你经常会在向量数据库文档中看到"余弦距离"。这简单地计算为 `(1 - 余弦相似度)`。对于余弦距离：

* 接近0的值表示高相似度
* 较大的值表示较低的相似度

这种调整使数字在许多情况下更容易解释。

## 步骤6：创建最终提示

最后，我们获取用户的问题和我们找到的最相关的文本块，将它们组合成一个提示，并将其发送给Claude以获得响应。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542288%2F07_-_004_-_The_Full_RAG_Flow_19.1748542288831.jpg)

提示可能如下所示：

```
回答用户关于财务文档的问题。

<user_question>
工程师今年修复了多少bug？
</user_question>

<report>
## 第2部分：软件工程
该部门投入了大量精力研究我们分布式系统中的各种感染向量
</report>
```

这就是完整的RAG管道！系统成功地基于语义相似度检索了最相关的信息，并将其作为上下文提供以生成准确的响应。

# 实现RAG流程

现在我们从概念上理解了RAG流程，让我们逐步实现它。我们将通过一个完整的例子来演示如何分块文本、生成嵌入、将它们存储在向量数据库中以及执行相似度搜索。

## 五步RAG实现

我们的实现遵循我们之前讨论的相同五个步骤：

1. 按章节分块文本
2. 为每个块生成嵌入
3. 创建向量存储并将每个嵌入添加到其中
4. 为用户的问题生成嵌入
5. 搜索存储以找到最相关的块

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542271%2F07_-_005_-_Implementing_the_Rag_Flow_10.1748542271657.jpg)

此图显示了我们如何将用户查询转换为嵌入并搜索向量数据库以找到最相关的内容。

## 步骤1：分块文本

首先，我们加载文档并将其分成可管理的部分：

```
with open("./report.md", "r") as f:
    text = f.read()

chunks = chunk_by_section(text)
chunks[2]  # 测试查看目录
```

我们使用之前的 `chunk_by_section`函数将文档分成逻辑部分。

## 步骤2：生成嵌入

接下来，我们一次性为所有块创建嵌入：

```
embeddings = generate_embedding(chunks)
```

嵌入函数已更新为可以处理单个字符串和字符串列表，使批处理更高效。

## 步骤3：存储在向量数据库中

现在我们创建向量存储并用嵌入及其关联的文本填充它：

```
store = VectorIndex()

for embedding, chunk in zip(embeddings, chunks):
    store.add_vector(embedding, {"content": chunk})
```

注意，我们同时存储嵌入和原始文本内容。这很关键，因为当我们稍后搜索时，我们需要返回实际文本，而不仅仅是数值嵌入值。

## 为什么要存储原始文本？

当我们查询向量数据库时，仅获取嵌入数字是没有用的。我们需要用于生成这些嵌入的实际文本。这就是为什么我们在数据库中的每个嵌入旁边包含原始块文本（或至少对它的引用）。

## 步骤4：处理用户查询

当用户提出问题时，我们为他们的查询生成嵌入：

```
user_embedding = generate_embedding("What did the software engineering dept do last year?")
```

## 步骤5：查找相关内容

最后，我们搜索向量存储以找到最相似的块：

```
results = store.search(user_embedding, 2)

for doc, distance in results:
    print(distance, "\n", doc["content"][0:200], "\n")
```

此搜索返回两个最相关的块及其相似度分数（余弦距离）。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542272%2F07_-_005_-_Implementing_the_Rag_Flow_12.1748542272138.jpg)

搜索结果向我们显示文档的哪些部分与用户的问题最相关，以及相似度分数。

## 理解结果

当我们运行关于软件工程部门的示例查询时，我们得到：

* **第2部分：软件工程** 距离为0.71（最接近的匹配）
* **方法论部分** 距离为0.72（第二接近）

较低的距离值表示较高的相似度，因此第2部分与我们的查询最相关。

## 下一步是什么？

这个实现对基本情况效果很好，但在某些情况下它的表现不如预期。在接下来的部分中，我们将探索改进措施，使我们的RAG系统更加健壮和准确。

关键要点是，RAG从根本上是关于将文本转换为数字（嵌入），有效地存储这些数字，然后在用户提出问题时使用数学相似度来找到相关内容。

# BM25词法搜索

在构建RAG管道时，你会很快发现仅靠语义搜索并不总是返回最佳结果。有时你需要语义搜索可能遗漏的精确术语匹配。解决方案是使用一种称为BM25的技术将语义搜索与词法搜索相结合。

## 仅使用语义搜索的问题

假设你在文档中搜索特定的事件ID，如"INC-2023-Q4-011"。虽然语义搜索擅长理解上下文和含义，但它可能返回语义相关但实际上不包含你要查找的确切术语的部分。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542341%2F07_-_006_-_BM25_Lexical_Search_05.1748542341261.jpg)

在上面的例子中，语义搜索返回了网络安全部分（确实包含事件ID），但也返回了根本没有提到该事件的财务分析部分。这是因为语义搜索关注概念相似性而不是精确术语匹配。

## 混合搜索策略

解决方案是并行运行语义搜索和词法搜索，然后合并结果。这为你提供了两全其美的方案：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542341%2F07_-_006_-_BM25_Lexical_Search_06.1748542341685.jpg)

* **语义搜索** 使用嵌入查找概念相关的内容
* **词法搜索** 使用经典文本搜索查找精确术语匹配
* **合并结果** 结合两种方法以获得更好的准确性

## BM25的工作原理

BM25（最佳匹配25）是RAG系统中用于词法搜索的流行算法。以下是它处理搜索查询的方式：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542342%2F07_-_006_-_BM25_Lexical_Search_07.1748542342052.jpg)

**步骤1：对查询进行分词**
将用户的问题分解为单个术语。例如，"a INC-2023-Q4-011"变成["a", "INC-2023-Q4-011"]。

**步骤2：计算术语频率**
查看每个术语在所有文档中出现的频率。常见词如"a"可能出现5次，而特定术语如"INC-2023-Q4-011"可能只出现一次。

**步骤3：按重要性加权术语**
出现频率较低的术语获得更高的重要性分数。单词"a"获得低重要性，因为它很常见，而"INC-2023-Q4-011"获得高重要性，因为它很罕见。

**步骤4：找到最佳匹配**
返回包含更多高权重术语实例的文档。

## 实现BM25搜索

以下是如何设置基本的BM25搜索系统：

```
# 1. 按章节分块文本
chunks = chunk_by_section(text)

# 2. 创建BM25存储并添加文档
store = BM25Index()
for chunk in chunks:
    store.add_document({"content": chunk})

# 3. 搜索存储
results = store.search("What happened with INC-2023-Q4-011?", 3)

# 打印结果
for doc, distance in results:
    print(distance, "\n", doc["content"][:200], "\n----\n")
```

当你运行此搜索时，你会得到比单独使用语义搜索好得多的结果。BM25算法优先考虑实际包含你的特定搜索术语的部分，特别是像事件ID这样的罕见术语。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542342%2F07_-_006_-_BM25_Lexical_Search_16.1748542342415.jpg)

注意结果现在如何正确地优先考虑软件工程部分和网络安全部分——这两个部分实际上都包含你要搜索的事件ID。

## 为什么这样效果更好

BM25擅长找到精确匹配，因为它：

* 对罕见的特定术语赋予更高的权重
* 忽略不增加搜索价值的常见词
* 关注术语频率而不是语义含义
* 对技术术语、ID和特定短语特别有效

关键见解是两种搜索方法具有互补的优势。语义搜索理解上下文和含义，而词法搜索确保你不会错过精确的术语匹配。通过结合它们，你创建了一个更强大的搜索系统，可以有效地处理概念查询和特定查找。

在下一步中，你将学习如何合并两个搜索系统的结果以创建统一的混合搜索体验。

# 多索引RAG管道

我们已经为语义搜索（使用向量嵌入）和词法搜索（使用BM25）构建了单独的实现。现在是时候将它们组合成一个统一的搜索管道，利用两种方法的优势。

## 多索引架构

我们的VectorIndex和BM25Index类共享几乎相同的API——它们都有 `add_document()`和 `search()`方法。这种一致性使得将它们包装在一个名为Retriever的新类中变得简单。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542335%2F07_-_007_-_A_Multi-Index_Rag_Pipeline_00.1748542335419.jpg)

Retriever充当协调器，将用户查询转发到两个索引，收集它们的结果，并使用一种称为倒数排名融合的技术合并它们。

## 理解倒数排名融合

合并来自不同搜索方法的结果并不像简单地连接列表那么简单。每种方法使用不同的评分系统，因此我们需要一种方法来公平地规范化和组合它们的排名。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542336%2F07_-_007_-_A_Multi-Index_Rag_Pipeline_04.1748542335890.jpg)

以下是倒数排名融合如何工作的示例。假设我们搜索有关"INC-2023-Q4-011"的信息并得到这些结果：

* VectorIndex返回：第2部分（排名1），第7部分（排名2），第6部分（排名3）
* BM25Index返回：第6部分（排名1），第2部分（排名2），第7部分（排名3）

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542336%2F07_-_007_-_A_Multi-Index_Rag_Pipeline_05.1748542336309.jpg)

我们将这些组合成一个表格，显示每个文本块在两个索引中的排名，然后应用RRF公式：

```
RRF_score(d) = Σ(1 / (k + rank_i(d)))
```

其中k是一个常数（通常为60，但我们将使用1以获得更清晰的结果），rank_i(d)是文档d在第i个排名中的排名。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542336%2F07_-_007_-_A_Multi-Index_Rag_Pipeline_06.1748542336704.jpg)

对于我们的例子：

* 第2部分：1.0/(1+1) + 1.0/(1+2) = 0.833
* 第7部分：1.0/(1+2) + 1.0/(1+3) = 0.583
* 第6部分：1.0/(1+3) + 1.0/(1+1) = 0.75

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542337%2F07_-_007_-_A_Multi-Index_Rag_Pipeline_08.1748542337402.jpg)

最终排名变为：第2部分（0.833），第6部分（0.75），第7部分（0.583）。这在直觉上是有道理的——第2部分在两个索引中都表现良好，因此它升到了顶部。

## 实现细节

Retriever类包装多个搜索索引并提供统一的接口：

```
class Retriever:
    def __init__(self, *indexes: SearchIndex):
        if len(indexes) == 0:
            raise ValueError("At least one index must be provided")
        self._indexes = list(indexes)

    def add_document(self, document: Dict[str, Any]):
        for index in self._indexes:
            index.add_document(document)

    def search(self, query_text: str, k: int = 1, k_rrf: int = 60):
        # 从所有索引获取结果
        all_results = []
        for idx, results in enumerate(all_results):
            for rank, (doc, _) in enumerate(results):
                # 跨索引跟踪文档排名
                # 应用RRF评分公式
        # 返回合并和排序的结果
```

关键见解是，通过在不同的搜索实现中保持一致的API，我们可以轻松地组合它们而无需紧密耦合。

## 测试混合方法

还记得我们之前的问题吗？搜索"what happened with INC-2023-Q4-011?"从仅向量方法返回了意外的结果？网络安全事件（第10部分）排在第一位，但财务分析（第3部分）排在第二位，而不是更相关的软件工程部分。

使用我们的混合检索器，我们现在得到了更好的结果：

* 第10部分：网络安全分析 - 事件响应报告（最相关）
* 第2部分：软件工程 - Phoenix项目稳定性增强（第二相关）
* 第5部分：法律发展（第三）

这展示了结合语义搜索和词法搜索如何克服单独使用任一方法的局限性。

## 可扩展性

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542337%2F07_-_007_-_A_Multi-Index_Rag_Pipeline_18.1748542337748.jpg)

这种架构的美妙之处在于其可扩展性。由于所有索引都实现了具有 `add_document()`和 `search()`方法的相同SearchIndex协议，你可以轻松添加新的搜索方法：

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542338%2F07_-_007_-_A_Multi-Index_Rag_Pipeline_19.1748542338538.jpg)

想要添加基于关键字的索引？基于图的搜索？专门的领域索引？只需实现相同的接口，Retriever就会自动将其纳入融合过程。

这种模块化方法使每个搜索实现保持专注和可测试，同时提供了一种在最终系统中结合它们优势的干净方式。

# 重新排序结果

我们构建的混合检索方法效果很好，但仍有一些弱点。当搜索"what did the eng team do with INC-2023-Q4-011?"时，我们可能期望软件工程部分排名更高，因为它特别提到了工程团队和事件。然而，当前系统仍然首先返回网络安全部分。

这就是重新排序的用武之地——一种添加另一个后处理步骤以提高检索准确性的技术。

## 重新排序如何工作

重新排序在概念上很简单。在运行向量索引和BM25索引并合并结果后，你添加一个步骤：使用Claude智能地重新排序搜索结果的重新排序器。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542387%2F07_-_008_-_Reranking_Results_05.1748542387152.jpg)

该过程的工作方式如下：

* 从混合搜索中获取合并的结果
* 将它们与用户的原始问题一起发送给Claude
* 要求Claude按相关性递减的顺序返回最相关的文档
* 使用Claude重新排序的列表作为最终结果

## 重新排序提示

提示结构很简单。你向Claude提供用户的问题和所有看起来相关的文档，然后要求执行一个简单的任务：

```
你的任务是找到与用户问题最相关的文档。

<user_question>
INC-2023-Q4-011发生了什么？
</user_question>

以下是可能相关的文档：
<documents>
<document>Section 10...</document>
<document>Section 2...</document>
<document>Section 7...</document>
<document>Section 6...</document>
</documents>

按相关性递减的顺序返回3个最相关的文档。
```

## 效率考虑

在实现重新排序时有一个重要的效率考虑。如果你要求Claude返回每个相关块的完整文本，你实际上是在要求它将大量文本复制回给你。这是浪费且缓慢的。

更好的方法是提前为每个文本块分配一个唯一的ID，然后要求Claude仅按正确的顺序返回这些ID：

```
<documents>
<document>
<id>ab84</id>
<content>Section 10...</content>
</document>
<document>
<id>51n3</id>
<content>Section 8...</content>
</document>
</documents>
```

然后Claude可以返回一个简单的列表，如 `["1p5g", "51n3", "ab83"]`，而不是复制整个文本块。

## 实现

重新排序函数在初始混合搜索完成后由检索器自动调用。以下是基本结构：

```
def reranker_fn(docs, query_text, k):
    # 使用ID格式化文档
    joined_docs = "\n".join([
        f"""
        <document>
        <document_id>{doc["id"]}</document_id>
        <document_content>{doc["content"]}</document_content>
        </document>
        """
        for doc in docs
    ])

    # 创建提示并获取Claude的响应
    prompt = f"""..."""
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, """```json""")

    result = chat(messages, stop_sequences=["""```"""])

    return json.loads(result["text"])["document_ids"]
```

## 请求报文和响应报文
### 请求
```json
{
  "max_tokens": 1000,
  "messages": [
    {
      "role": "user",
      "content": "<见下方多行文本>"
    },
    {
      "role": "assistant",
      "content": "```json"
    }
  ],
  "model": "gemini-3-flash",
  "stop_sequences": [
    "```"
  ],
  "temperature": 1
}
```

**user message 的 content 内容（多行格式）：**

```
    你将收到一组文档及各自 id。请从中选出与用户问题最相关的 2 篇，并按相关度从高到低排序。

    用户问题：
    <question>
    工程团队是如何处理 INC-2023-Q4-011 的？
    </question>

    候选文档：
    <documents>
    
        <document>
        <document_id>cGSz</document_id>
        <document_content>第二节：软件工程——Project Phoenix 稳定性提升

软件工程部门投入大量精力提升支撑 Project Phoenix 的核心系统的稳定性与性能。反复出现的问题，尤其是高峰负载下的 `ERR_MEM_ALLOC_FAIL_0x8007000E` 以及影响数据检索的 `TIMEOUT_QUERY_DB_0xDEADBEEF`，被列为优先处理项，对应事件成本为 INC-2023-Q4-011。根因分析指向主数据缓存算法的低效以及数据库索引策略欠佳。补丁部署解决了内存分配错误，在 2024 年第四季度模拟压力测试中（测试用例 ID：INC-2023-Q4-011）测得关键故障减少约 40%。查询模块的进一步重构已安排在下一发布周期，旨在解决超时问题。这些发现凸显了健全测试流程的重要性，尤其考虑到产品工程团队（第六节）所识别的依赖关系。团队继续密切监控系统遥测，以发现任何回归或新出现的错误模式。2024 年第四季度，团队还协助处理了 INC-2023-Q4-011 事件。
</document_content>
        </document>
        

        <document>
        <document_id>4LUp</document_id>
        <document_content>第十节：网络安全分析——事件响应报告：INC-2023-Q4-011

网络安全运营中心成功遏制并修复了编号为 `INC-2023-Q4-011` 的定向入侵尝试。威胁情报显示，该活动与 `ShadowNet Syndicate` 威胁行为者组织的战术、技术与程序相符。初始访问通过针对财务部门人员的鱼叉式钓鱼邮件获得，可能意在获取与第三节（财务分析）相关的数据。端点检测与响应（EDR）系统在工作站 `WS-FIN-112` 上标记了异常进程执行（`PID：7812`）。后续调查发现恶意软件（`SHA256：e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`）试图向服务器 `SRV-FIN-03` 横向移动。遏制措施包括隔离受影响系统并封锁相关指挥与控制基础设施（IP `198.51.100.24`）。缓解措施包括部署更新的端点策略并实施增强的边界过滤（防火墙规则 ID：FN7832）。该事件凸显了持续的威胁态势以及对持续警惕和用户培训的需求，尤其涉及敏感的财务及潜在研究数据（如第一节、第九节）。取证分析仍在进行中。
</document_content>
        </document>
        
    </documents>

    请严格按以下 JSON 格式回复（仅返回 JSON，不要其他说明）：
    ```json
    {
        "document_ids": ["id1", "id2", ...]   // 共 2 个文档 id，按与问题的相关度从高到低排列，最相关的排在最前
    }
    ```
```
### 响应
```json
{
  "id": "Bk2RaaP3FOCojuMP_Iv_qAo",
  "type": "message",
  "role": "assistant",
  "model": "gemini-3-flash",
  "content": [
    {
      "type": "text",
      "text": "\n{\n    \"document_ids\": [\"cGSz\", \"4LUp\"]\n}\n```"
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 936,
    "output_tokens": 23,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0
  }
}
```

## 结果

当使用"what did the eng team do with INC-2023-Q4-011?"测试重新排序方法时，软件工程部分现在出现在结果的第一位。Claude成功地识别出用户的查询特别关心工程团队及其与事件的关系。

## 权衡

重新排序带来明显的权衡：

* **增加的延迟：** 你现在必须等待对Claude的额外API调用
* **提高的准确性：** Claude可以以纯向量相似度无法做到的方式理解上下文和相关性

对于大多数应用程序，准确性的提高值得延迟成本，特别是当你处理复杂查询时，语义理解比纯关键字匹配更重要。

# 上下文检索

上下文检索是一种通过解决一个基本问题来提高RAG管道准确性的技术：当你将文档分成块时，每个块都会失去与更广泛文档上下文的连接。

## 标准分块的问题

当你获取源文档并将其分解成块以用于向量数据库时，每个单独的部分不再知道它来自哪里或它与文档其余部分的关系。这可能会损害检索准确性，因为块缺少重要的上下文信息。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542388%2F07_-_009_-_Contextual_Retrieval_00.1748542388165.jpg)

## 上下文检索如何工作

上下文检索在将块插入检索器数据库之前添加了一个预处理步骤。以下是该过程：

* 获取每个单独的块和原始源文档
* 将两者与特定提示一起发送给Claude
* 要求Claude编写一个简短的片段，将块置于整个文档中
* 将此上下文与原始块结合以创建"上下文化块"
* 在向量和BM25索引中使用上下文化块

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542389%2F07_-_009_-_Contextual_Retrieval_05.1748542389149.jpg)

提示要求Claude分析块并编写上下文，解释块相对于更大文档的内容。例如，如果你有一个关于软件工程的部分提到了2023年的事件，Claude可能会生成上下文，解释该部分来自更大的报告，并且同一事件也在其他部分中提到。

## 处理大型文档

一个常见的问题是当你的源文档太大而无法放入Claude的单个提示中。在这种情况下，你可以提供一组减少的上下文而不是整个文档。

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542389%2F07_-_009_-_Contextual_Retrieval_08.1748542389514.jpg)

策略是包括：

* 文档开头的几个块（通常包含摘要或摘要）
* 你正在上下文化的块之前的块
* 跳过中间与当前块不太相关的块

这种方法为Claude提供了足够的上下文来理解文档的内容以及当前块如何适应，而不会用不必要的文本压倒提示。

## 实现示例

以下是为单个块添加上下文的基本函数：

```
def add_context(text_chunk, source_text):
    prompt = """
    编写一个简短而简洁的文本片段，将此块置于整个源文档中，以改进块的搜索检索。

    以下是原始源文档：
    <document>
    {source_text}
    </document>

    以下是我们想要置于整个文档中的块：
    <chunk>
    {text_chunk}
    </chunk>

    仅用简洁的上下文回答，不要其他内容。
    """

    messages = []
    add_user_message(messages, prompt)
    result = chat(messages)

    return result["text"] + "\n" + text_chunk
```

对于使用有限上下文处理多个块，你可以选择要包含的特定块：

```
# 为每个块添加上下文，然后添加到检索器
num_start_chunks = 2
num_prev_chunks = 2

for i, chunk in enumerate(chunks):
    context_parts = []

    # 文档开头的初始块集
    context_parts.extend(chunks[: min(num_start_chunks, len(chunks))])

    # 我们正在上下文化的当前块之前的额外块
    start_idx = max(0, i - num_prev_chunks)
    context_parts.extend(chunks[start_idx:i])

    context = "\n".join(context_parts)

    contextualized_chunk = add_context(chunk, context)
    retriever.add_document({"content": contextualized_chunk})
```

## 预期结果

当你使用上下文检索运行搜索查询时，你将获得包含生成的上下文和原始块内容的结果。上下文帮助检索系统更好地理解每个块的内容以及它与更广泛文档的关系。

例如，上下文化块可能以以下内容开头："此块是年度跨学科研究评审的第2部分，详细说明了解决Phoenix项目稳定性问题的软件工程工作..."，然后是原始块文本。

这种技术对于复杂文档特别有价值，其中各个部分有许多相互连接和对文档其他部分的引用。添加的上下文有助于确保即使搜索查询与块的原始文本不完全匹配，也能检索到相关块。
