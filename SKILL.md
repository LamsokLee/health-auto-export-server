---
name: health-auto-export-server
description: >-
  Run a Flask REST API server to receive Apple Health data from the Health Auto Export iOS app.
  Saves incoming JSON/CSV health data to a configured directory. Use when setting up health data
  ingestion from iPhone, running the health receiver server, configuring Health Auto Export app,
  or troubleshooting health data sync issues.
---

# Health Auto Export Server

Simple Flask server that receives health data from the iOS Health Auto Export app and saves it to disk.

## Quick Start

```bash
python3 skills/health-auto-export-server/receive_server.py
```

Server starts on `http://0.0.0.0:3000/health-data`

## Configuration

Environment variables (optional):

| Variable | Meaning |
|----------|---------|
| `HEALTH_DATA_DIR` | Directory for saved JSON/CSV. If unset, defaults to `health-export-data/` next to `receive_server.py`. |
| `PORT` | Listen port (default `3000`). |

```bash
export HEALTH_DATA_DIR="/path/to/health/data"
export PORT=3000
python3 skills/health-auto-export-server/receive_server.py
```

## Docker (NAS / home server)

Build and run from `skills/health-auto-export-server/`:

```bash
cd skills/health-auto-export-server
docker compose up -d --build
```

- **Data**: map a host folder to `/data` (see `docker-compose.yml` — `HEALTH_EXPORT_DATA` or edit the volume).
- **URL on phone**: `http://<NAS_LAN_IP>:3000/health-data` (or set `HOST_PORT` if 3000 is taken).
- Image uses **Gunicorn** + Flask; same env vars as above inside the container.

Details: [setup.md](setup.md#docker-nas--synology).

## iPhone Setup

1. Install Health Auto Export app
2. Create new REST API automation
3. Set URL to `http://YOUR_MAC_IP:3000/health-data`
4. Select metrics to export (JSON format, Version 2)
5. Set sync cadence (daily recommended)

## Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health-data` | POST | Receive health data (JSON or CSV) |
| `/health-data` | GET | Health check / server status |

## File Output

Saved files are named:
- `{app_name}_{timestamp}.json` for JSON data
- `{app_name}_{timestamp}.csv` for CSV uploads

## Full Setup Guide

See [setup.md](setup.md) for detailed iPhone configuration and troubleshooting.

## Integration

This server pairs with:
- **health-data-importer** skill — load saved JSON into DuckDB for analysis
- Obsidian vault health tracking system

## Pipeline

1. **Receive** (this skill): iPhone → `receive_server.py` → Raw JSON files
2. **Import** (health-data-importer): Raw JSON → DuckDB

After receiving data, import into DuckDB:

```bash
python3 skills/health-data-importer/duckdb-importer.py "/path/to/Raw"
```

## Troubleshooting

- **Connection failed**: Check Mac IP, same Wi-Fi, firewall
- **No data received**: Ensure Health Auto Export has Health permissions
- **Background sync fails**: iOS restrictions — use manual export or iPhone Mirroring
