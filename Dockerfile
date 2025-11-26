FROM python:3.11-slim

LABEL maintainer="Serenium Team <team@serenium.org>"
LABEL description="Serenium Package Builder - Production-ready package scaffolding tool"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV SERENIUM_VERSION=1.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    debhelper \
    dh-python \
    devscripts \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY serenium.py .
COPY themes.py .

# Install the package in development mode
RUN pip install -e .

# Create non-root user
RUN useradd --create-home --shell /bin/bash serenium
USER serenium

# Set entrypoint
ENTRYPOINT ["serenium"]
CMD ["--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD serenium --version || exit 1
