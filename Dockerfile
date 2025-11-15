# ============================================
# Stage 1: Base image with Python runtime
# ============================================
FROM python:3.12-slim AS runtime

# Ensure Python output is unbuffered (good for logging)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set a working directory inside the container
WORKDIR /app

# Install system dependencies (if needed later, we keep it minimal for now)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install Python deps
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and config into the image
COPY app ./app
COPY config ./config

# Default SQLite DB location will be /app/health.db
# (matches your current settings: sqlite:///./health.db)

# Expose the FastAPI port
EXPOSE 8000

# Environment variables for configuration (can be overridden at run-time)
# These match your pydantic-settings fields:
# - db_url
# - health_check_interval_seconds
# - services_config_path
ENV DB_URL="sqlite:///./health.db" \
    HEALTH_CHECK_INTERVAL_SECONDS=60 \
    SERVICES_CONFIG_PATH="config/services.json"

# Start the FastAPI app using Uvicorn
# Using 0.0.0.0 so it's reachable from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
