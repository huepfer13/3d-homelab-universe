---
name: 3d-homelab-universe
description: Use to integrate the 3D Spiderweb Universe dashboard. Drop config.json, serve with any HTTP server, embed in iframes or kiosk displays.
category: creative
---

# 3D Spiderweb Universe Integration

Config-driven Three.js dashboard — galaxies, solar systems, animated packets. Drop your own `config.json`, no code changes.

## Quick Start

```bash
python3 -m http.server 8000
# Open http://localhost:8000/universe.html
```

## Embedding

### Iframe
```html
<iframe src="http://your-host:8000/universe.html" width="100%" height="600" frameborder="0"></iframe>
```

### Kiosk Mode (Chromium)
```bash
chromium --kiosk --no-first-run http://your-host:8000/universe.html
```

## Configuration (`config.json`)

```json
{
  "title": "My Dashboard",
  "galaxies": [{ "id":"g1","name":"Node A","x":-25,"y":0,"z":-10,"r":12,"color":39423 }],
  "systems": [{ "id":"s1","name":"Service","g":"g1","x":-6,"y":6,"z":-3,"r":5,"color":65535 }],
  "connections": [["s1","s2"]],
  "packets": [{ "type":"issue","title":"Bug #42","status":"Open","from":"s1","to":"s2","speed":0.003 }]
}
```

### Packet Types
| Type   | Color  | Use Case |
|--------|--------|----------|
| issue  | Magenta | Tickets, bugs |
| deploy | Cyan   | Builds, releases |
| error  | Red    | Alerts, failures |
| ping   | Dim    | Heartbeats |
| data   | Orange | Sync, transfers |

## Tests
```bash
python3 test_universe.py
```
11 unit tests cover config validation, HTML structure, feature detection.

## License
MIT
