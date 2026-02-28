import json
from typing import Optional, Literal, List
from mcp.types import CallToolResult, Tool, TextContent
from mcp_client import MCPClient
from anthropic.types import Message, ToolResultBlockParam

from core.log_config import get_logger

_logger = get_logger("tools")


class ToolManager:
    @classmethod
    async def get_all_tools(cls, clients: dict[str, MCPClient]) -> list[Tool]:
        """Gets all tools from the provided clients."""
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            tools += [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema,
                }
                for t in tool_models
            ]
        _logger.info("get_all_tools: %s", [f"{t['name']}: {t['description']})" for t in tools])
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        """Finds the first client that has the specified tool."""
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                _logger.debug("_find_client_with_tool: found %s", tool_name)
                return client
        _logger.warning("_find_client_with_tool: not found %s", tool_name)
        return None

    @classmethod
    def _build_tool_result_part(
        cls,
        tool_use_id: str,
        text: str,
        status: Literal["success"] | Literal["error"],
    ) -> ToolResultBlockParam:
        """Builds a tool result part dictionary."""
        return {
            "tool_use_id": tool_use_id,
            "type": "tool_result",
            "content": text,
            "is_error": status == "error",
        }

    @classmethod
    async def execute_tool_requests(
        cls, clients: dict[str, MCPClient], message: Message
    ) -> List[ToolResultBlockParam]:
        """Executes a list of tool requests against the provided clients."""
        tool_requests = [
            block for block in message.content if block.type == "tool_use"
        ]
        _logger.info(
            "execute_tool_requests: count=%d ids,names,inputs=%s",
            len(tool_requests),
            [f"{r.id}: {r.name}: {json.dumps(r.input, indent=2, ensure_ascii=False)}" for r in tool_requests],
        )
        tool_result_blocks: list[ToolResultBlockParam] = []
        for tool_request in tool_requests:
            tool_use_id = tool_request.id
            tool_name = tool_request.name
            tool_input = tool_request.input

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                _logger.warning("execute_tool_requests: no client for %s", tool_name)
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id, "Could not find that tool", "error"
                )
                tool_result_blocks.append(tool_result_part)
                continue

            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = []
                if tool_output:
                    items = tool_output.content
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                content_json = json.dumps(content_list, ensure_ascii=False)
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id,
                    content_json,
                    "error"
                    if tool_output and tool_output.isError
                    else "success",
                )
                _logger.info(
                    "execute_tool_requests: %s status=%s content_json=%s",
                    tool_name,
                    "error" if (tool_output and tool_output.isError) else "success",
                    content_json,
                )
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {e}"
                _logger.error("%s", error_message)
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id,
                    json.dumps({"error": error_message}, ensure_ascii=False),
                    "error",
                )

            tool_result_blocks.append(tool_result_part)
        _logger.info("execute_tool_requests: tool_result_blocks=%s", json.dumps(tool_result_blocks, indent=2, ensure_ascii=False))
        return tool_result_blocks
