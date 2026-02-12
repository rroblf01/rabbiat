from mcp.server.fastmcp import FastMCP

server = FastMCP("Example MCP Server")


@server.tool()
async def database_status(name: str) -> str:
    return "online" if name == "main_db" else "offline"


if __name__ == "__main__":
    server.run()
