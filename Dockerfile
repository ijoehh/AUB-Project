# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Create virtual environment in /opt/venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy backend requirements and install dependencies into virtual environment
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user named app with fixed UID 1000
RUN useradd -u 1000 -m app

# Copy app source code and set ownership
COPY --chown=app:app backend/app /app/app
COPY --chown=app:app backend/data /app/data

# Ensure ownership of the app directory is set to app
RUN chown -R app:app /app

EXPOSE 8000

# Health check using Python standard library
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

# Switch to non-root user app before CMD
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
