# Health Auto Export receiver — runs Gunicorn + Flask
FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HEALTH_DATA_DIR=/data \
    PORT=3000

COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY receive_server.py .

EXPOSE 3000

# Run as root so bind mounts on NAS/Synology stay writable without UID tuning.

# PORT and worker count tunable via env
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT} --workers ${GUNICORN_WORKERS:-2} --threads ${GUNICORN_THREADS:-2} --timeout 120 receive_server:app"]
