# Health Auto Export - REST API Setup

## Server Setup (Mac)

### 1. Start the Receiver Server

```bash
cd /path/to/workspace
python3 skills/health-auto-export-server/receive_server.py
```

Server will start on `http://YOUR_MAC_IP:3000`

### 2. Find Your Mac's IP Address

```bash
ipconfig getifaddr en0
```

Or check System Settings → Network

---

## Docker (NAS / Synology)

Run the receiver on a NAS or always-on Linux box so the phone targets a stable LAN URL.

### Files

| File | Role |
|------|------|
| `Dockerfile` | Python 3.12 + Gunicorn + Flask |
| `docker-compose.yml` | Port publish, `/data` volume, env |
| `requirements-docker.txt` | Image dependencies |

### Build and start

```bash
cd skills/health-auto-export-server
docker compose up -d --build
```

### Persist exports on the NAS

Edit `docker-compose.yml` (or set env when invoking compose) so the **left** side of the volume is a folder on the NAS, for example:

```yaml
volumes:
  - /volume1/docker/health-auto-export:/data
```

Or from the shell:

```bash
export HEALTH_EXPORT_DATA=/volume1/docker/health-auto-export
docker compose up -d
```

Inside the container, `HEALTH_DATA_DIR` is `/data` (set in the Compose file).

### iPhone URL

Use your NAS **LAN** IP (same Wi‑Fi as the phone):

`http://192.168.x.x:3000/health-data`

If port 3000 is busy on the host, set `HOST_PORT` (e.g. `HOST_PORT=8080 docker compose up -d`) and use that port in the app.

### Firewall

Allow TCP **3000** (or `HOST_PORT`) from your LAN on the NAS/router if sync fails.

### Logs

```bash
docker compose logs -f health-auto-export
```

---

## iPhone Configuration (Health Auto Export)

### Create New Automation

1. Open **Health Auto Export** app
2. Go to **Automations** tab
3. Tap **"New Automation"**
4. Select **"REST API"**

### Configure Automation

**Basic Settings:**
- **Name:** `Obsidian Sync`
- **Notify When Run:** ON (optional)

**URL Configuration:**
- **URL:** `http://YOUR_MAC_IP:3000/health-data`
  - Example: `http://192.168.1.50:3000/health-data`
- **Timeout:** 30 seconds

**Headers:** (optional)
- None needed for basic setup

**Data Type:**
- Select **"Health Metrics"**
- Choose metrics to sync:
  - ✅ Step Count
  - ✅ Active Energy
  - ✅ Resting Heart Rate
  - ✅ Heart Rate
  - ✅ Sleep Analysis
  - ✅ Blood Oxygen (if you track it)
  - ✅ Body Mass (if you track it)

**Export Settings:**
- **Format:** JSON
- **Version:** Version 2
- **Date Range:** Yesterday (or "Since Last Sync")
- **Summarize Data:** ON
- **Time Grouping:** Days
- **Batch Requests:** OFF (for now)

**Sync Cadence:**
- **Frequency:** 1
- **Interval:** Day
- **Time:** 8:00 AM (or whenever you prefer)

---

## Testing

### Manual Test

1. In Health Auto Export, tap **"Manual Export"**
2. Select date range (try "Yesterday")
3. Tap **"Export"**
4. Check your Mac terminal for received data

### Verify Data

After successful sync, check the save directory:
- `~/SynologyDrive/Obsidian/Linshuo-Memory/04-Health/09-Auto-Export/Raw/`

---

## Troubleshooting

### "Connection Failed" on iPhone

1. Check Mac IP address hasn't changed
2. Ensure server is running (`python3 receive_server.py`)
3. Verify both devices on same Wi-Fi
4. Check Mac firewall allows port 3000

### "No Data Received"

1. Open Health Auto Export and let it sync with Apple Health first
2. Try "Manual Export" with "Previous 7 Days"
3. Check Activity Logs in the app

### Background Sync Limitations

iOS restricts background processing:
- Sync may not run at exact scheduled time
- Low Power Mode prevents background sync
- Device must be unlocked for health data access

**Solution:** Manual export when you open the app

---

## Tips for Best Results

### Keep Data Fresh

**Option A: iPhone Mirroring (Recommended)**
- Use iPhone Mirroring on macOS
- Keeps app "active" for more frequent syncs

**Option B: Manual Sync Habit**
- Open Health Auto Export each morning
- Tap "Manual Export" → "Yesterday"
- Quick and reliable

---

## Next Steps

1. ✅ Start server on Mac
2. ✅ Configure automation on iPhone
3. ✅ Test with manual export
4. ⬜ Load data into DuckDB (see health-data-importer skill)
5. ⬜ Set up daily habit (open app + sync)
6. ⬜ Add more metrics as needed

---

## Integration

This server pairs with:
- **health-data-importer** skill — load saved JSON into DuckDB for analysis
- Obsidian vault health tracking system

---

*Last updated: 2026-04-04*