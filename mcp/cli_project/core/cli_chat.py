from typing import List, Tuple
from mcp.types import Prompt, PromptMessage
from anthropic.types import MessageParam

from core.chat import Chat
from core.claude import Claude
from mcp_client import MCPClient
import json
from core.log_config import get_logger

_logger = get_logger("cli_chat")


class CliChat(Chat):
    def __init__(
        self,
        doc_client: MCPClient,
        clients: dict[str, MCPClient],
        claude_service: Claude,
    ):
        super().__init__(clients=clients, claude_service=claude_service)

        self.doc_client: MCPClient = doc_client
        _logger.info("CliChat.__init__")

    async def list_prompts(self) -> list[Prompt]:
        prompts = await self.doc_client.list_prompts()
        _logger.info("list_prompts: count=%d", len(prompts))
        return prompts

    async def list_docs_ids(self) -> list[str]:
        ids = await self.doc_client.read_resource("docs://documents")
        _logger.info("list_docs_ids: count=%d", len(ids))
        return ids

    async def get_doc_content(self, doc_id: str) -> str:
        content = await self.doc_client.read_resource(f"docs://documents/{doc_id}")
        _logger.debug("get_doc_content: doc_id=%s len=%d", doc_id, len(content))
        return content

    async def get_prompt(
        self, command: str, doc_id: str
    ) -> list[PromptMessage]:
        messages = await self.doc_client.get_prompt(command, {"doc_id": doc_id})
        _logger.info("get_prompt: command=%s doc_id=%s count=%d", command, doc_id, len(messages))
        return messages

    async def _extract_resources(self, query: str) -> str:
        mentions = [word[1:] for word in query.split() if word.startswith("@")]

        doc_ids = await self.list_docs_ids()
        mentioned_docs: list[Tuple[str, str]] = []

        for doc_id in doc_ids:
            if doc_id in mentions:
                content = await self.get_doc_content(doc_id)
                mentioned_docs.append((doc_id, content))

        _logger.debug(f"_extract_resources: mentions={mentions}   contents={json.dumps([content for doc_id, content in mentioned_docs], indent=2, ensure_ascii=False)}")
        return "".join(
            f'\n<document id="{doc_id}">\n{content}\n</document>\n'
            for doc_id, content in mentioned_docs
        )

    async def _process_command(self, query: str) -> bool:
        if not query.startswith("/"):
            return False

        words = query.split()
        command = words[0].replace("/", "")

        messages = await self.doc_client.get_prompt(
            command, {"doc_id": words[1]}
        )

        self.messages += convert_prompt_messages_to_message_params(messages)
        _logger.info("_process_command: command=%s doc_id=%s", command, words[1] if len(words) > 1 else None)
        return True

    async def _process_query(self, query: str):
        if await self._process_command(query):
            return

        added_resources = await self._extract_resources(query)
        _logger.info("_process_query: free-form query, resources_len=%d", len(added_resources))

        prompt = f"""
        用户的问题如下：
        <query>
        {query}
        </query>

        以下上下文可能有助于回答：
        <context>
        {added_resources}
        </context>

        说明：用户问题中可能包含对文档的引用，例如「@report.docx」。@ 仅用于提及文档，实际文档名为「report.docx」。
        若上述上下文中已包含该文档内容，则无需再调用工具读取。请直接、简洁地回答用户问题，先给出他们最需要的信息。
        不要复述或提及「根据上述上下文」等表述，仅用上下文内容来支撑你的回答即可。
        """

        self.messages.append({"role": "user", "content": prompt})


def convert_prompt_message_to_message_param(
    prompt_message: "PromptMessage",
) -> MessageParam:
    role = "user" if prompt_message.role == "user" else "assistant"

    content = prompt_message.content

    # Check if content is a dict-like object with a "type" field
    if isinstance(content, dict) or hasattr(content, "__dict__"):
        content_type = (
            content.get("type", None)
            if isinstance(content, dict)
            else getattr(content, "type", None)
        )
        if content_type == "text":
            content_text = (
                content.get("text", "")
                if isinstance(content, dict)
                else getattr(content, "text", "")
            )
            return {"role": role, "content": content_text}

    if isinstance(content, list):
        text_blocks = []
        for item in content:
            # Check if item is a dict-like object with a "type" field
            if isinstance(item, dict) or hasattr(item, "__dict__"):
                item_type = (
                    item.get("type", None)
                    if isinstance(item, dict)
                    else getattr(item, "type", None)
                )
                if item_type == "text":
                    item_text = (
                        item.get("text", "")
                        if isinstance(item, dict)
                        else getattr(item, "text", "")
                    )
                    text_blocks.append({"type": "text", "text": item_text})

        if text_blocks:
            return {"role": role, "content": text_blocks}

    return {"role": role, "content": ""}


def convert_prompt_messages_to_message_params(
    prompt_messages: List[PromptMessage],
) -> List[MessageParam]:
    return [
        convert_prompt_message_to_message_param(msg) for msg in prompt_messages
    ]
