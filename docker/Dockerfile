FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

# Install the application dependencies.
COPY ../pyproject.toml ../uv.lock ./
RUN uv sync --frozen --no-cache

ENV PATH="/app/.venv/bin:$PATH"

# Copy the application into the container.
COPY ../ /app

# Copy entrypoint script and make it executable
COPY docker/web_entrypoint.sh /web_entrypoint.sh
RUN chmod +x /web_entrypoint.sh

ENTRYPOINT ["/web_entrypoint.sh"]


