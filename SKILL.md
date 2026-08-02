---
name: 3d-homelab-universe-dashboard
description: Deploy 3D spiderweb dashboard from config.json.
category: creative
trigger: Dashboard setup, 3D visualization, kiosk mode
---

# 3D Spiderweb Universe Dashboard

Config-driven Three.js dashboard — galaxies, solar systems, animated packets with trails. Drop your own `config.json`, no code changes needed.

## Quick Start
```bash
git clone https://github.com/huepfer13/3d-homelab-universe.git
cd 3d-homelab-universe
python3 -m http.server 8000
# Open http://localhost:8000/universe.html
```

## Kiosk Mode — Vollbild-Display ohne Browser-Chrome

### Chromium (Linux/macOS/Windows)
```bash
# Vollbild, keine Tab-Leiste, kein erstmaliges Setup-Popup
chromium --kiosk --no-first-run --disable-infobars --disable-session-crashed-bubble \
  --disable-translate --no-default-browser-check \
  http://your-host:8000/universe.html
```

### Chromium mit Autostart (Linux Desktop)
```bash
# ~/.config/autostart/universe-kiosk.desktop
[Desktop Entry]
Type=Application
Name=3D Universe Kiosk
Exec=chromium --kiosk --no-first-run --disable-infobars --disable-session-crashed-bubble --disable-translate --no-default-browser-check http://192.168.2.184:9120/
X-GNOME-Autostart-enabled=true
```

### Systemd Kiosk Service (headless display)
```ini
# /etc/systemd/system/universe-kiosk.service
[Unit]
Description=3D Universe Kiosk Display
After=graphical.target

[Service]
Type=simple
User=kiosk
Environment=DISPLAY=:0
ExecStart=/usr/bin/chromium --kiosk --no-first-run --disable-infobars --disable-session-crashed-bubble --disable-translate --no-default-browser-check http://your-host:8000/universe.html
Restart=always
RestartSec=10

[Install]
WantedBy=graphical.target
```

### Raspberry Pi / ARM
```bash
# Chromium im Kiosk-Mode ohne GPU-Beschleunigung (fallback)
chromium-browser --kiosk --no-first-run --disable-gpu --disable-software-rasterizer \
  http://your-host:8000/universe.html
```

### Firefox Kiosk
```bash
firefox --kiosk http://your-host:8000/universe.html
```

### Acemagic Display (unser Setup)
```bash
# Läuft auf xomni (192.168.2.191) via User-Systemd-Service
# Dashboard hosted auf CT 105 (192.168.2.184:9120)
chromium --kiosk --no-first-run --disable-infobars \
  http://192.168.2.184:9120/
```

### Troubleshooting Kiosk
| Problem | Lösung |
|---------|--------|
| Schwarzer Bildschirm | `--disable-gpu` oder `--disable-software-rasterizer` |
| "Chrome wurde nicht sauber beendet" | `--disable-session-crashed-bubble` |
| Mauszeiger sichtbar | `--disable-mouse-cursor` (nicht standard) |
| Falsche Auflösung | `--window-size=1920,1080` oder `--start-fullscreen` |
| WebGL-Fehler | GPU-Treiber prüfen, `--ignore-gpu-blocklist` |

## Integration Patterns

### Iframe Embed
```html
<iframe src="http://<host>:8000/universe.html" width="100%" height="600" frameborder="0"></iframe>
```

### Live API Integration
Create a `/api/universe-state` endpoint returning:
```json
{"nodes":[],"pipeline":[],"paperless":{"docs":1289},"issues_open":5}
```
The dashboard polls this endpoint every 30s via `fetch()`.

## Tests
```bash
cd 3d-homelab-universe && python3 test_universe.py  # 11 unit tests
```

## Configuration (`config.json`)
- `galaxies`: top-level nodes (clusters/servers) with x, y, z, radius, color
- `systems`: child services inside galaxies, each referencing a parent galaxy ID
- `connections`: [fromId, toId] pairs linking systems
- `packets`: animated data with type (issue/deploy/error/ping/data), title, status, from, to, speed

## Known Issue
[#1 Stale verification engine](https://github.com/huepfer13/3d-homelab-universe/issues/1).

## License
MIT — [Repository](https://github.com/huepfer13/3d-homelab-universe)
