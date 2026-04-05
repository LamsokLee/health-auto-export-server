#!/usr/bin/env python3
"""
Health Auto Export file saver
Flask receiver that saves Health Auto Export payloads to disk without processing.
"""

from flask import Flask, request, jsonify
from datetime import datetime
from pathlib import Path
import json
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration — HEALTH_DATA_DIR in .env (see .env.example); Docker sets it in compose
_save_default = os.environ.get("HEALTH_DATA_DIR")
if _save_default:
    SAVE_DIR = Path(_save_default).expanduser()
else:
    SAVE_DIR = (Path(__file__).resolve().parent / "health-export-data").resolve()
SAVE_DIR.mkdir(parents=True, exist_ok=True)

PORT = int(os.environ.get("PORT", "3000"))


def _write_bytes_atomic(path: Path, data: bytes) -> None:
    """Write via temp file + rename. Some NAS sync daemons (e.g. Synology Drive) observe renames reliably."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / f".{path.name}.{os.getpid()}.tmp"
    try:
        with open(tmp, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
        raise


@app.route('/health-data', methods=['POST'])
def receive_health_data():
    """Receive health data and save to file"""
    
    headers = dict(request.headers)
    content_type = headers.get('Content-Type', '').lower()
    
    # Get timestamp for filename (includes date)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Get app name from header (optional)
    app_name = headers.get('automation-name', '').replace(' ', '')
    if app_name:
        app_name = f"{app_name}_"
    
    # Determine format and save
    if 'multipart/form-data' in content_type:
        # CSV file upload
        if request.files:
            file_key = list(request.files.keys())[0]
            file = request.files[file_key]
            raw_data = file.read()
            
            # Save as CSV
            filename = f"{app_name}{timestamp}.csv"
            filepath = SAVE_DIR / filename
            _write_bytes_atomic(filepath, raw_data)
            
            print(f"[{timestamp}] Saved CSV: {filename} ({len(raw_data)} bytes)")
            return jsonify({'status': 'success', 'filename': filename, 'size': len(raw_data)})
        
    elif 'json' in content_type:
        # JSON data
        data = request.json
        raw_data = json.dumps(data, indent=2).encode('utf-8')
        
        # Save as JSON
        filename = f"{app_name}{timestamp}.json"
        filepath = SAVE_DIR / filename
        _write_bytes_atomic(filepath, raw_data)
        
        print(f"[{timestamp}] Saved JSON: {filename} ({len(raw_data)} bytes)")
        return jsonify({'status': 'success', 'filename': filename, 'size': len(raw_data)})
    
    # Unknown format, try to save raw data
    raw_data = request.data
    if raw_data:
        filename = f"{app_name}{timestamp}.bin"
        filepath = SAVE_DIR / filename
        _write_bytes_atomic(filepath, raw_data)
        
        print(f"[{timestamp}] Saved binary: {filename} ({len(raw_data)} bytes)")
        return jsonify({'status': 'success', 'filename': filename, 'size': len(raw_data)})
    
    return jsonify({'status': 'error', 'message': 'No data received'}), 400


@app.route('/health-data', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'save_directory': str(SAVE_DIR),
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Health Auto Export File Saver")
    print("=" * 60)
    print(f"Save directory: {SAVE_DIR}")
    print("-" * 60)
    print(f"Server running on http://0.0.0.0:{PORT}")
    print("Ready to receive health data...")
    print("=" * 60)

    app.run(host="0.0.0.0", port=PORT, debug=False)