from mcp.server.fastmcp import FastMCP

server = FastMCP("Example MCP Server")


@server.tool()
async def all_users() -> list[str]:
    return ["Alice", "Bob", "Charlie"]


if __name__ == "__main__":
    server.run()
