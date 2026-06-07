FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libpq-dev \
    # PySide6 display dependencies (for running frontend in container via X11)
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxcb-xinerama0 \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Install uv — modern, fast Python package manager (replaces pip for speed)
# New tool worth knowing: uv is written in Rust and 10-100x faster than pip
RUN pip install uv

WORKDIR /workspace

# Install Ruff and mypy globally so they're available immediately
RUN pip install ruff mypy

# Keep container running
CMD ["sleep", "infinity"]
