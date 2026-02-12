"""
ASGI config for rabbiat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rabbiat.settings")

django_app = get_asgi_application()

app = Starlette()
app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    ),
    name="static",
)
app.mount("/", django_app)

application = app
