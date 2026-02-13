FROM python:3.14.3-slim-trixie


ENV WORKDIR /app
WORKDIR $WORKDIR
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"

COPY pyproject.toml /tmp/pyproject.toml

RUN rm /usr/local/bin/pip
COPY --from=ghcr.io/astral-sh/uv:0.10.2-python3.14-trixie-slim /usr/local/bin/uv /usr/local/bin/uv
RUN uv pip install --system -r /tmp/pyproject.toml
COPY . $WORKDIR

CMD ["daphne", "rabbiat.asgi:application", "--bind", "0.0.0.0", "--port", "8000"]