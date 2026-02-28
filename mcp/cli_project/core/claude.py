from anthropic import Anthropic
from anthropic.types import Message
import os
import json

from core.log_config import get_logger

_logger = get_logger("claude")


#
class Claude:
    def __init__(self, base_url: str, api_key: str, model: str):
        claude_code_headers = {
            "User-Agent": "claude-code/2.1.39",
            "X-Stainless-Lang": "js",
            "X-Stainless-Package-Version": "0.52.0",
            "X-Stainless-OS": "MacOS",
            "X-Stainless-Arch": "arm64",
            "X-Stainless-Runtime": "node",
            "X-Stainless-Runtime-Version": "v22.13.1",
            "X-Stainless-Async": "async:promise",
        }
        self.client = Anthropic(api_key=api_key, base_url=base_url, default_headers=claude_code_headers)
        self.model = model
        _logger.info("Claude.__init__: base_url=%s model=%s", base_url, model)

    def add_user_message(self, messages: list, message):
        user_message = {
            "role": "user",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(user_message)
        _logger.debug("add_user_message: len(messages)=%d", len(messages))

    def add_assistant_message(self, messages: list, message):
        assistant_message = {
            "role": "assistant",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(assistant_message)
        _logger.debug("add_assistant_message: len(messages)=%d", len(messages))

    def text_from_message(self, message: Message):
        return "\n".join(
            [block.text for block in message.content if block.type == "text"]
        )

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ) -> Message:
        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences,
        }
       
       
        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        _logger.info(
            "chat: model=%s messages=%d tools=%s",
            self.model,
            len(messages),
            len(tools) if tools else 0,
        )
        _log_body = json.dumps(
            params,
            indent=2,
            ensure_ascii=False,
            default=lambda o: o.content if isinstance(o, Message) else str(o),
        )
        _logger.debug("chat:request params=%s", _log_body.replace("\\n", "\n"))

        message = self.client.messages.create(**params)
        _resp_body = json.dumps(
            message.model_dump(),
            indent=2,
            ensure_ascii=False,
            default=lambda o: getattr(o, "content", str(o)) if hasattr(o, "content") else str(o),
        )
        _logger.debug("chat:response=%s", _resp_body.replace("\\n", "\n"))
        _logger.debug("chat: response stop_reason=%s", getattr(message, "stop_reason", None))
        return message
