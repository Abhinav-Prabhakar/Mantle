# syntax=docker/dockerfile:1
# Build context: the repo root.  Targets: api (default runtime), train (adds torch for retraining).
FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never PYTHONUNBUFFERED=1 \
    PATH=/app/backend/.venv/bin:$PATH
WORKDIR /app/backend
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 curl && rm -rf /var/lib/apt/lists/*
COPY backend/pyproject.toml backend/uv.lock backend/.python-version ./
COPY backend/packages packages

# ---- build stage: compilers for sdists (ecos, from scikit-survival) stay out of the runtime image
FROM base AS build-api
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN uv sync --frozen --no-dev --package mantle-api

# ---- serving image: only what the API needs (no torch; M3/M6 run on onnxruntime)
FROM base AS api
COPY --from=build-api /app/backend/.venv .venv
COPY backend/models models
COPY backend/data/reference data/reference
# the synthetic database is built inside the image from the seeds; the parquet is dropped afterwards
RUN mantle-data build --only S1,S2,S5 --scale default \
 && rm -rf data/synthetic data/processed
ENV MANTLE_API_HOST=0.0.0.0 MANTLE_API_PORT=8000 MANTLE_DATA_DIR=/var/mantle MANTLE_DB_SEED=/app/backend/data/mantle.duckdb
VOLUME /var/mantle
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s --start-period=60s --retries=6 \
  CMD curl -fsS http://localhost:8000/api/health || exit 1
CMD ["mantle-api"]

# ---- retraining image (docker compose --profile train): adds the torch stack
FROM base AS train
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN uv sync --frozen --no-dev --package mantle-ml --extra train
COPY backend/models models
COPY backend/data/reference data/reference
ENV MANTLE_DATA_DIR=/var/mantle
CMD ["mantle-ml", "train", "--all"]
