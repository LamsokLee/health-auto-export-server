# Health Auto Export — REST receiver

Small **Flask** service that accepts Apple Health exports from the [Health Auto Export](https://www.healthyapps.com/health-auto-export/) iOS app (REST API automation) and saves **JSON** or **CSV** to disk.

Designed to run in **Docker** on a NAS or home server so your phone can POST to a stable URL on your LAN.

## Quick start (Docker)

```bash
docker compose up -d --build
```

Point the app at: `http://<server-lan-ip>:3000/health-data`

Copy [`.env.example`](.env.example) to `.env` and adjust `HEALTH_EXPORT_DATA` (host folder for exports) and `HOST_PORT` if needed.

### Build the image only

```bash
docker build -t health-auto-export-server:latest .
```

### Persist data on the host

The compose file mounts `${HEALTH_EXPORT_DATA:-./health-export-data}` → `/data` in the container. Set a NAS path in `.env`, for example:

```bash
HEALTH_EXPORT_DATA=/volume1/docker/health-auto-export
```

Inside the container, `HEALTH_DATA_DIR` is `/data` (set in `docker-compose.yml`).

### Firewall and logs

Allow TCP **3000** (or `HOST_PORT`) from your LAN if sync fails.

```bash
docker compose logs -f health-auto-export
```

## Optional: run with Python (local dev)

```bash
pip install -r requirements.txt
cp .env.example .env   # optional; set HEALTH_DATA_DIR / PORT
python receive_server.py
```

Same URL pattern: `http://<host-ip>:3000/health-data`

## iPhone — Health Auto Export

1. Open **Health Auto Export** → **Automations** → **New Automation** → **REST API**.

**URL:** `http://<SERVER_IP>:3000/health-data` (use `HOST_PORT` if you changed it). Timeout ~30s.

**Data type:** Health Metrics — pick the metrics you care about.

**Export:** Format **JSON**, **Version 2**, date range e.g. Yesterday or Since Last Sync, **Summarize Data** on, **Time Grouping** Days, **Batch Requests** off unless you know you need it.

**Schedule:** e.g. daily at a fixed time (background sync may be delayed by iOS).

### Manual test

Use **Manual Export** in the app with a short range (e.g. Yesterday), then check the host folder you mounted for new `.json` / `.csv` files.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/health-data` | Receive export payload |
| GET | `/health-data` | Health check + configured save directory |

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `HEALTH_DATA_DIR` | `./health-export-data` next to the script (local only) | Output directory inside the process |
| `PORT` | `3000` | HTTP port (Gunicorn / dev server) |
| `HEALTH_EXPORT_DATA` | `./health-export-data` | **Compose:** host path mounted at `/data` |
| `HOST_PORT` | `3000` | **Compose:** published host port |
| `GUNICORN_WORKERS` | `2` | **Docker** |
| `GUNICORN_THREADS` | `2` | **Docker** |

## Saved files

- `{automation-name}_{timestamp}.json` — JSON
- `{automation-name}_{timestamp}.csv` — CSV upload  
  (`automation-name` comes from the `automation-name` header when set.)

## Troubleshooting

- **Connection failed:** Server IP, same Wi‑Fi, firewall, correct port.
- **No data received:** Health permissions in the app, try Manual Export / wider date range, check app activity logs.
- **Background sync:** iOS may defer work; Low Power Mode and lock state matter. Manual export or iPhone Mirroring on Mac often helps.

## Downstream

Pair with a **health-data-importer** (or similar) to load saved JSON into DuckDB or another store. Obsidian or note workflows can point at the same export directory.

## License

Use and modify for personal use; no warranty.
