FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for persistence
RUN mkdir -p /app/data /app/backups /app/logs

# Set permissions
RUN chmod 755 /app/data /app/backups /app/logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Environment variables for production
ENV ENVIRONMENT=production
ENV DATABASE_PATH=/app/data/tec_database.db
ENV BACKUP_ENABLED=true
ENV LOG_LEVEL=INFO

# Start command
CMD ["python", "tec_persona_api.py"]
