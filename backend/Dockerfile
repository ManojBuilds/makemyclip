# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies including ffmpeg and unzip (for deno)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install deno (required by yt-dlp for YouTube JS challenge solving)
RUN curl -fsSL https://deno.land/install.sh | sh
ENV DENO_DIR=/root/.deno
ENV PATH="/root/.deno/bin:${PATH}"

# Install uv package manager
RUN pip install uv

# Force UV to use CPU-only torch index to reduce image size from 8GB+ to <2GB
ENV UV_EXTRA_INDEX_URL="https://download.pytorch.org/whl/cpu"
ENV UV_INDEX_STRATEGY="unsafe-best-match"
ENV UV_HTTP_TIMEOUT=300

# Set working directory
WORKDIR /app

# Copy pyproject.toml and uv.lock for dependency installation
COPY pyproject.toml uv.lock* ./

# Sync dependencies and clean cache in one step
RUN uv sync --no-cache

# Force update yt-dlp to the absolute latest version to handle YouTube API changes
RUN uv pip install --upgrade --force-reinstall yt-dlp "yt-dlp[default]"

# Copy source code
COPY src/ ./src/

# Copy fonts and transitions directories
COPY fonts/ ./fonts/
COPY transitions/ ./transitions/

# Copy and prepare production start script
COPY start_prod.sh ./
RUN chmod +x ./start_prod.sh

# Create necessary directories for video processing
RUN mkdir -p /app/uploads /app/clips /app/logs /tmp

# Expose the port (FastAPI/Railway default)
EXPOSE 8080

# Start the application using the multi-process script
CMD ["./start_prod.sh"]
