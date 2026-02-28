from mcp.server.fastmcp import FastMCP

# 初始化服务端
app = FastMCP("my-server")

# 注册一个供客户端调用的方法
@app.tool()
async def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    app.run(transport="stdio")
