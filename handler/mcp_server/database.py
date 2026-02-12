import os
import sys
import django
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async

server = FastMCP("Example MCP Server for Database Access")


@server.tool()
async def get_user(username: str):
    from django.contrib.auth.models import User

    try:
        return await User.objects.aget(username=username)
    except User.DoesNotExist:
        return None


@server.tool()
async def list_usersname():
    from django.contrib.auth.models import User

    return await sync_to_async(
        lambda: list(User.objects.values_list("username", flat=True))
    )()


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rabbiat.settings")
    django.setup()
    server.run()
