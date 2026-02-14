FROM python:3.14.3-slim-trixie

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock /app/

RUN uv pip install --system -r /app/pyproject.toml

COPY . .

ENTRYPOINT [ "daphne", "rabbiat.asgi:application", "--bind", "0.0.0.0", "--port", "8000" ] 