import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

async def main():
    # 1. 定义子进程的启动命令和参数
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    # 2. 启动子进程，接管 stdin/stdout
    async with stdio_client(server_params) as (read_stream, write_stream):
        # 3. 建立 JSON-RPC 会话
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # 4. 发起调用 (内部自动封装为 JSON-RPC 2.0 并解析响应)
            result = await session.call_tool("add", arguments={"a": 10, "b": 20})

            # 提取并打印结果
            print(f"服务端计算结果: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
