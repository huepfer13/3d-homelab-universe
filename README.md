# 🌌 3D Spiderweb Universe Dashboard

[![Tests](https://img.shields.io/badge/tests-11%2F11-brightgreen)](test_universe.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Three.js](https://img.shields.io/badge/Three.js-r128-00ffcc)](https://threejs.org/)

> **Deutsch:** Universelles, konfigurationsgetriebenes 3D-Dashboard für Infrastruktur-Visualisierung. Galaxien, Sonnensysteme und animierte Datenpakete — einfach eigene `config.json` ablegen, kein Code-Änderung nötig.
>
> **English:** Universal, config-driven 3D dashboard for infrastructure visualization. Galaxies, solar systems, and animated data packets — drop your own `config.json`, no code changes needed.

---

## ✨ Features / Funktionen

| Feature | Description |
|---------|-------------|
| 🌌 **Hierarchical Nesting** | Galaxies → Solar Systems → Planets. Strict parent-child scene graph. |
| 🖱️ **OrbitControls** | Drag to rotate, scroll to zoom, right-drag to pan. Damped for smooth navigation. |
| 🎯 **Click-to-Center** | Click any object to shift the universe — that object becomes the new origin. |
| 💫 **Oscillating Rotation** | Universe, galaxies, and systems rotate with `Math.sin()` — no drift off-screen. |
| 🔮 **3D Multi-Axis Halos** | Three orthogonal rings (XY, XZ, YZ) per node with **AdditiveBlending** — true 3D volume from any camera angle. |
| 🌫️ **Packet Fade-In/Out** | Packets fade opacity at halo entry/exit points — visual depth cue. |
| 📊 **Color-Coded Packets** | issue (magenta), deploy (cyan), error (red), ping (dim), data (orange) with AdditiveBlending trails. |
| 🔴 **Pulsing Load Rings** | Green ring pulses with system load. |
| 🔍 **Permanent Labels** | HTML labels projected from 3D coordinates — always visible, no hover needed. |
| 🏴 **Crosshair** | Fixed center crosshair marks the origin `(0,0,0)`. |
| 📄 **Config-Driven** | Everything in `config.json`. No code changes for custom deployments. |
| 📋 **Accordion Hierarchy** | Expandable legend showing galaxies and systems — click to focus any node. |
| 📡 **Pipeline Badge** | HUD shows live CI/CD pipeline status with color coding. |
| 📜 **Event Log** | Streaming event stream with timestamps, color-coded by severity. |
| 🖱️ **Hover Tooltips** | Mouse-over nodes to see metadata (type, radius, parent galaxy). |
| 🌐 **Live API** | Polls `/api/universe-state` every 30s for real-time HUD data. |
| 🔗 **Connection Types** | active (solid cyan), ping (dim dashed), tube (curved red/orange arc). |

---

## 🚀 Quick Start (DE/EN)

```bash
git clone https://github.com/huepfer13/3d-homelab-universe.git
cd 3d-homelab-universe
python3 -m http.server 8000
# Open http://localhost:8000/universe.html
```

---

## 🧪 Tests

```bash
python3 test_universe.py
# 11 tests: config validation, HTML structure, feature detection, no hardcoded IPs
```

---

## 🔧 Integration Patterns

### Iframe Embed
```html
<iframe src="http://your-host:8000/universe.html" width="100%" height="600" frameborder="0"></iframe>
```

### Kiosk Mode (Chromium)
```bash
chromium --kiosk --no-first-run --disable-infobars http://your-host:8000/universe.html
```

### Systemd Service (DE)
```bash
# /etc/systemd/system/universe-dashboard.service
[Unit]
Description=3D Universe Dashboard
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 -m http.server 8000 --directory /opt/universe
Restart=always

[Install]
WantedBy=default.target
```

### Live API (JSON endpoint)
The dashboard polls `/api/universe-state` every 30s. Serve this endpoint alongside the HTML:
```json
{
  "nodes": [{"name":"node1","online":true}],
  "pipeline": [{"title":"CI Build","conclusion":"success"}],
  "paperless": {"docs":1289},
  "issues_open": 5
}
```

---

## 📁 Project Structure / Projektstruktur

```
3d-homelab-universe/
├── universe.html          # Main dashboard (Three.js, self-contained)
├── config.json            # Example configuration (real homelab topology)
├── test_universe.py       # 11 unit tests
├── SKILL.md               # Hermes Agent skill definition
├── README.md              # This file (DE + EN)
├── LICENSE                # MIT License
├── CHANGELOG.md           # Version history
└── .github/
    └── ISSUE_TEMPLATE/
        └── bug_report.md
```

---

## 🎨 Architecture / Architektur

```
Scene
└── UniverseGroup (U)
    ├── Galaxy "acemagic"     ← Node 1
    │   ├── Core (sphere)
    │   ├── 3-Axis Halo (XY, XZ, YZ rings, AdditiveBlending)
    │   ├── Load Ring (pulsing green)
    │   └── Solar Systems (CTs/VMs)
    │       ├── 3-Axis Bubble (XY/XZ/YZ, AdditiveBlending)
    │       ├── Core (sphere)
    │       └── Orbit line to galaxy center
    ├── Galaxy "proxmox"      ← Node 2
    │   └── ...
    └── Galaxy "xshaka"      ← Node 3
        └── ...
```

### Data Flow / Datenfluss
```
config.json  →  init(C)  →  3D Scene  →  animate() loop
     ↑                            ↓
  User edits              Live API poll
                          (/api/universe-state)
```

---

## 🐛 Known Issues / Bekannte Probleme

- [#1 Stale Verification Engine](https://github.com/huepfer13/3d-homelab-universe/issues/1): Hermes Agent's first-hash cache ignores subsequent verifications. Seeking community input.

---

## 📜 License / Lizenz

MIT License — see [LICENSE](LICENSE) for full text.

**Third-party dependencies:**
- [Three.js](https://threejs.org/) r128 (MIT License), loaded from CDN
- [OrbitControls](https://threejs.org/examples/#misc_controls_orbit) (MIT License), loaded from CDN

---

## 🤝 Contributing

Contributions welcome! Open an [issue](https://github.com/huepfer13/3d-homelab-universe/issues) or submit a PR.

### Development
1. Fork the repo
2. Edit `config.json` for your topology
3. Run `python3 test_universe.py` to validate
4. Submit PR with description

---

*Built with ❤️ for infrastructure monitoring. Powered by Three.js.*
