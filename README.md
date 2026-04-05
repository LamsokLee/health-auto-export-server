# Health Auto Export — REST receiver

Small **Flask** service that accepts Apple Health exports from the [Health Auto Export](https://www.healthyapps.com/health-auto-export/) iOS app (REST API automation) and saves **JSON** or **CSV** to disk.

Use on a Mac, Linux box, or **NAS** (Docker) so your phone can POST to a stable URL on your LAN.

## Quick start (Python)

```bash
pip install -r requirements.txt
export HEALTH_DATA_DIR=/path/to/save/dir   # optional; default: ./health-export-data next to the script
export PORT=3000                            # optional
python receive_server.py
```

Health Auto Export URL: `http://<host-ip>:3000/health-data`

## Docker / NAS

```bash
docker compose up -d --build
```

See [setup.md](setup.md) for iPhone configuration, firewall notes, and Synology-oriented volume examples.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/health-data` | Receive export payload |
| GET | `/health-data` | Health check + configured save directory |

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `HEALTH_DATA_DIR` | `./health-export-data` (next to `receive_server.py`) | Output directory |
| `PORT` | `3000` | HTTP port (dev server) |
| `GUNICORN_WORKERS` | `2` | Docker only |
| `GUNICORN_THREADS` | `2` | Docker only |

## License

Use and modify for personal use; no warranty.
