import os
import sys
import django
from mcp.server.fastmcp import FastMCP

server = FastMCP("Example MCP Server for Creating Prompts")


@server.tool()
async def create_prompt(name: str, text: str):
    from handler.models import Prompt, AIModel

    model = await AIModel.objects.aget(name="gemini-3-flash-preview")

    await Prompt.objects.acreate(name=name, text=text, model=model)

    return f"Prompt '{name}' creado exitosamente."


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rabbiat.settings")
    django.setup()
    server.run()
