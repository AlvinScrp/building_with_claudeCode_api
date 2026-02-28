import asyncio
import sys
import os
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
from core.log_config import setup_logging
from core.claude import Claude

from core.cli_chat import CliChat
from core.cli import CliApp

load_dotenv()
setup_logging()

# Anthropic Config
claude_model = os.getenv("CLAUDE_MODEL", "")
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert base_url, "Error: BASE_URL cannot be empty. Update .env"
assert api_key, "Error: API_KEY cannot be empty. Update .env"


async def main():
    claude_service = Claude(base_url=base_url, api_key=api_key, model=claude_model)

    server_scripts = sys.argv[1:]
    clients = {}

    command, args = (
        ("uv", ["run", "mcp_server.py"])
        if os.getenv("USE_UV", "0") == "1"
        else ("python", ["mcp_server.py"])
    )

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(
                MCPClient(command="uv", args=["run", server_script])
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
