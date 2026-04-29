# Stage 1: Build stage
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

# Set environment variables for uv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_HTTP_TIMEOUT=300

WORKDIR /app

# Install build dependencies (only if needed for C-extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and uv.lock for dependency installation
COPY pyproject.toml uv.lock* ./

# Sync dependencies (excluding dev dependencies)
RUN uv sync --frozen --no-dev --no-install-project --no-cache

# Force update yt-dlp to the absolute latest version to handle YouTube API changes
RUN uv pip install --upgrade --force-reinstall yt-dlp "yt-dlp[default]"


# Stage 2: Runtime stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/.venv/bin:/root/.deno/bin:$PATH"
ENV DENO_DIR=/root/.deno

WORKDIR /app

# Install runtime dependencies including ffmpeg and libraries for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    unzip \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install deno (required by yt-dlp for YouTube JS challenge solving)
RUN curl -fsSL https://deno.land/install.sh | sh

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code and static assets
COPY src/ ./src/
COPY fonts/ ./fonts/
COPY transitions/ ./transitions/
COPY start_prod.sh ./

# Prepare production start script and directories
RUN chmod +x ./start_prod.sh && \
    mkdir -p /app/uploads /app/clips /app/logs /tmp

# Expose the port (FastAPI/Railway default)
EXPOSE 8080

# Start the application using the multi-process script
CMD ["./start_prod.sh"]
