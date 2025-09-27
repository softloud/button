# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y \
    graphviz \
    graphviz-dev \
    gcc \
    g++ \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first (for better Docker layer caching)
COPY pyproject.toml ./
COPY uv.lock ./

# Install uv (fast Python package manager)
RUN pip install uv

# Install dependencies using uv
RUN uv pip install --system -r pyproject.toml

# Copy the entire application
COPY button_1/ ./button_1/
COPY README.md ./

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash gameuser
RUN chown -R gameuser:gameuser /app
USER gameuser

# Set the default command to run the game
CMD ["python", "-m", "button_1"]

# Expose port 8000 in case we want to add a web interface later
EXPOSE 8000

# Add labels for better container management
LABEL maintainer="your-email@example.com"
LABEL description="Press A Button Now - Satirical Data Science Adventure Game"
LABEL version="1.0.0"