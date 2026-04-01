from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional

from .config import APIConfig, create_client
from .prompts import build_system_prompt
from .tools import ToolExecutor


class ScaffoldAgent:
    def __init__(
        self,
        config: APIConfig,
        workspace: Path | str = ".",
        ask_user_fn: Optional[Callable[[str], str]] = None,
        max_loops: int = 20,
    ) -> None:
        self.config = config
        self.client = create_client(config)
        self.tools = ToolExecutor(workspace=workspace, ask_user_fn=ask_user_fn)
        self.system_prompt = build_system_prompt()
        self.max_loops = max_loops

    def run(self, user_request: str) -> str:
        if not user_request.strip():
            raise ValueError("用户请求不能为空")

        messages: list[dict[str, Any]] = [{"role": "user", "content": user_request}]

        for _ in range(self.max_loops):
            response = self._request_message(messages=messages)

            assistant_blocks = [self._normalize_block(block) for block in response.content]
            messages.append({"role": "assistant", "content": assistant_blocks})

            tool_calls = [block for block in assistant_blocks if block.get("type") == "tool_use"]
            if not tool_calls:
                text = self._collect_text(assistant_blocks)
                return text or "任务已完成。"

            tool_results = []
            for tool_call in tool_calls:
                tool_use_id = tool_call.get("id")
                tool_name = tool_call.get("name", "")
                tool_input = tool_call.get("input", {})
                result_text = self.tools.execute_for_model(tool_name=tool_name, tool_input=tool_input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result_text,
                    }
                )

            messages.append({"role": "user", "content": tool_results})

        return "达到最大循环次数，任务可能未完整执行。请细化请求后重试。"

    def _request_message(self, messages: list[dict[str, Any]]) -> Any:
        request_kwargs = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "system": self.system_prompt,
            "tools": self.tools.schemas(),
            "messages": messages,
        }
        try:
            return self.client.messages.create(**request_kwargs)
        except ValueError as exc:
            # New Anthropic SDK versions require streaming for long-running requests.
            if "Streaming is required" not in str(exc):
                raise
            with self.client.messages.stream(**request_kwargs) as stream:
                return stream.get_final_message()

    @staticmethod
    def _normalize_block(block: Any) -> dict[str, Any]:
        if isinstance(block, dict):
            return block
        if hasattr(block, "model_dump"):
            dumped = block.model_dump()
            if isinstance(dumped, dict):
                return dumped
        normalized: dict[str, Any] = {}
        for key in ("id", "type", "text", "name", "input"):
            value = getattr(block, key, None)
            if value is not None:
                normalized[key] = value
        return normalized

    @staticmethod
    def _collect_text(blocks: list[dict[str, Any]]) -> str:
        texts = [str(block.get("text", "")).strip() for block in blocks if block.get("type") == "text"]
        return "\n".join(part for part in texts if part)
