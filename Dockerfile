# Build stage
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

# Set the working directory
WORKDIR /app

# Copy project configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the project itself
RUN uv sync --locked --no-dev --no-install-project

# Copy the project
COPY . /app

# Install the project in non-editable mode
RUN uv sync --locked --no-dev --no-editable

# Final stage
FROM python:3.11-slim

# Create a non-root user
RUN useradd -r -u 1000 -m mcp-youtube

# Set the working directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder --chown=app:app /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use the non-root user
USER mcp-youtube

# Expose the default port
EXPOSE 8000

# Run the server
ENTRYPOINT ["mcp-youtube", "--transport", "sse", "--sse-address", "0.0.0.0:8000"]
