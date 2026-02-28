from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "这份证词记录涵盖了 Angela Smith（注册工程师 P.E.）的证言。",
    "report.pdf": "该报告详细说明了一座 20 米冷凝塔的状况。",
    "financials.docx": "这份财务资料概述了项目的预算和支出。",
    "outlook.pdf": "本文件展示了对未来绩效的预测。",
    "plan.md": "该计划概述了项目实施的步骤。",
    "spec.txt": "这些规格说明定义了设备的技术要求。"
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name="read_doc_contents",
    description="读取文档内容并以字符串形式返回。"
)
def read_document(
    doc_id: str = Field(description="要读取的文档 ID")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="通过将文档内容中的某段文字替换为新文字来编辑文档。"
)
def edit_document(
    doc_id: str = Field(description="将要被编辑的文档 ID"),
    old_str: str = Field(description="要被替换的文字，必须完全匹配（包括空格）。"),
    new_str: str = Field(description="用于替换原文字的新文字。")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

# TODO: Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="将文档内容重写为 Markdown 格式。"
)
def format_document(
    doc_id: str = Field(description="要格式化的文档 ID"),
) -> list[base.Message]:
    prompt = f"""
    你的目标是将文档用 Markdown 语法重新排版。

    需要重新排版的文档 ID 为：
    <document_id>
    {doc_id}
    </document_id>

    根据需要添加标题、列表、表格等。可以补充说明文字，但不要改变报告的原意。
    使用 'edit_document' 工具编辑文档。编辑完成后，直接回复文档的最终版本，不要解释你做了哪些修改。
    """

    return [base.UserMessage(prompt)]


# TODO: Write a prompt to summarize a doc
@mcp.prompt(
    name="summarize",
    description="对文档内容进行摘要。"
)
def summarize_document(
    doc_id: str = Field(description="要摘要的文档 ID"),
) -> list[base.Message]:
    prompt = f"""
    你的目标是对文档进行简明摘要。

    需要摘要的文档 ID 为：
    <document_id>
    {doc_id}
    </document_id>

    先用 'read_doc_contents' 工具读取文档，再对其内容做简要概括。
    """

    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
