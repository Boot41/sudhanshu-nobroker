# ---------- Stage 1: Build the React client ----------
FROM node:20-alpine AS client-builder

# Enable pnpm via corepack
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copy only package manager files first for better caching
COPY client/web/package.json ./
COPY client/web/pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy client source
COPY client/web .

# Build client (Vite outputs to dist by default)
RUN pnpm run build


# ---------- Stage 2: Python server with static file serving ----------
FROM python:3.11-slim AS server

# Install UV package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# System deps (optional, keep minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set workdir to project root inside the container
WORKDIR /app

# Copy server project as a package under /app/server so imports like `from server...` work
COPY server/ ./server/

# Move into server dir for dependency install with uv
WORKDIR /app/server

# Install Python dependencies using uv (locked)
COPY server/pyproject.toml server/uv.lock ./
RUN uv sync --frozen

# Optionally add whitenoise (if you plan to serve static files directly from FastAPI/Starlette)
# RUN uv add whitenoise

# Copy the rest of the server code (already copied above for context; keep to ensure fresh state)
# Note: Done earlier with COPY server/ ./server/

# Copy built client artifacts into server static directory
# Your FastAPI should mount this directory (e.g., at /assets) in main.py
RUN mkdir -p /app/server/static
COPY --from=client-builder /app/dist /app/server/static

# Create a startup script
RUN echo '#!/bin/sh\n\
export PYTHONPATH=/app:$PYTHONPATH\n\
# Uncomment if using Alembic migrations\n\
# uv run alembic upgrade head\n\
uv run uvicorn server.main:app --host 0.0.0.0 --port 8000' > /app/server/start.sh \
    && chmod +x /app/server/start.sh

EXPOSE 8000

ENV PYTHONPATH=/app
ENV STATIC_FILES_DIR=/app/server/static

# Default workdir is the server dir to run the app
WORKDIR /app/server

CMD ["/app/server/start.sh"]
