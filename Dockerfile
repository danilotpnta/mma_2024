# Dockerfile for mma_2024 (HuBERT Genre Classifier)
# Production-ready machine learning dashboard

FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code with correct ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 7864

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7864/ || exit 1

# Run the dashboard
# Adjust the command based on how your dashboard/src/main.py starts the server
# If it's Flask: CMD ["python", "dashboard/src/main.py"]
# If it's FastAPI with uvicorn: CMD ["uvicorn", "dashboard.src.main:app", "--host", "0.0.0.0", "--port", "7864"]
# If it's Streamlit: CMD ["streamlit", "run", "dashboard/src/main.py", "--server.port=7864", ...]
CMD ["python", "dashboard/src/main.py"]