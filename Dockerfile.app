FROM python:3.11-slim

# uv, same version as in development, to install the exact versions of uv.lock
COPY --from=ghcr.io/astral-sh/uv:0.12.21 /uv /bin/uv

WORKDIR /app

# Install the dependencies first so this layer is cached when only the code changes
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"

COPY src ./src
COPY bin ./bin

# 8001: API, 4201: Prefect server
EXPOSE 8001 4201

CMD ["bash", "bin/run_services.sh"]
