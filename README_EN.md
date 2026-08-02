# 🌌 3D Homelab Universe

> **Your entire homelab as a living, glowing sci-fi universe — at a glance.**
>
> 🚀 **[LIVE DEMO](https://huepfer13.github.io/3d-homelab-universe/)** — try it in your browser!

**3D Homelab Universe** transforms your servers, nodes, and containers into a stunning 3D galaxy with **5 galaxies × 5 containers** (25 systems total). Each object features **3 independent multi-metric halos** (X=CPU, Y=RAM, Z=Disk I/O) that change color and pulsation in real time. Data packets with trail history fly between nodes, the event stream logs all activity, and a single click zooms you to any container.

**No WebGL?** No problem — a Canvas2D fallback draws 25 animated dots on a 5×5 grid, ensuring you always see visual activity.

---

## 🚀 Quick Start

```bash
git clone https://github.com/huepfer13/3d-homelab-universe.git
cd 3d-homelab-universe
python3 -m http.server 8000
# Open http://localhost:8000/index.html
```

> 💡 **No cloning needed?** [Live demo on GitHub Pages](https://huepfer13.github.io/3d-homelab-universe/)

---

## ✨ Features

### 🪐 3D Universe
- **5 Galaxies** (Alpha..Epsilon) spread across X-axis (-40..+40)
- **25 Containers** (A1..A5, B1..B5, ..., E1..E5) with individual halos
- **OrbitControls**: Zoom, orbit, pan via mouse
- **Click-to-Center**: Click any container/galaxy to center the universe
- **Background double-click**: Reset to origin (0,0,0)
- **Crosshair HUD**: Permanently marks canvas center

### 📊 Multi-Metric Halos (NEW!)
Every container and galaxy has **3 orthogonal rings**:
| Ring | Axis | Metric | Color idle→busy→critical |
|------|------|--------|---------------------------|
| ⬤ Horizontal | X | **CPU** | cyan → orange → red |
| ⬤ Vertical | Y | **RAM** | cyan → orange → red |
| ⬤ Depth | Z | **Disk I/O** | cyan → orange → red |

- Rings pulse independently with metric-specific frequency
- Color transitions smoothly via `color.lerp()`
- Metrics drift randomly (simulated live data)
- **Legend** in HUD explains the mapping

### ☄️ Data Packets
- Flying packets with **trail history** (comet tail effect)
- **Fade-in/out** at start and end points
- Color-coded by type (Issue, Deploy, Error, Ping, Data)
- **Additive-blending** glow for sci-fi aesthetic

### 🧠 Event Stream
- Live log with timestamps and **color-coded status**
- **Expandable sub-tasks** (parent→child hierarchy)
- **Filter search** in event log
- Auto-cleanup: entries removed after 6 hours
- Direct **source linking**: click opens issue/link

### 📂 Hierarchy Accordion
- **Expandable**: Galaxies → Containers → Pipelines
- **Focus Node**: Click zooms to selected object
- Dynamically generated from `config.json`

### 🎨 Canvas2D Fallback
- When WebGL is unavailable (headless browsers, older GPUs):
  - 25 animated, pulsing dots on a 5×5 grid
  - Galaxy colors (blue tones)
  - Seamless transition: stops once WebGL is active

### ⚙️ Configuration (`config.json`)
- External JSON defines galaxies, containers, connections, packets
- **DE/EN help modal** with keyboard shortcuts and descriptions
- Colors, positions, sizes — all customizable

### 🔧 CI/CD (GitHub Actions)
- Runs **entirely on GitHub** — zero homelab resources
- `test_universe.py` unit tests on every push
- HTML validation (DOCTYPE, tags, structure)
- `config.json` validation (5 galaxies, 25 systems)

---

## 📁 Project Structure

```
├── index.html           # Dashboard (self-contained, 39 KB)
├── universe-3d.html     # 3D-only version
├── sim.html             # Minimal simulation
├── config.json          # 5 galaxies, 25 systems, connections
├── test_universe.py     # Unit tests
├── SKILL.md             # AI agent integration
├── .github/workflows/   # CI/CD pipeline
│   └── ci.yml
├── README.md            # German documentation
├── README_EN.md         # English documentation (this file)
├── CHANGELOG.md
└── LICENSE (MIT)
```

---

## 🎮 Controls

| Action | Input |
|--------|-------|
| Orbit (rotate) | Left mouse button + drag |
| Zoom | Scroll wheel |
| Pan (move) | Right mouse button + drag |
| Focus object | Click container/galaxy |
| Reset center | Double-click background |
| Center button | ⌖ CENTER UNIVERSE in HUD |
| Expand accordion | Click ▶ toggle |
| Event filter | Type in filter box |

---

## 🌍 Localization

- **German**: `README.md`, UI texts in dashboard
- **English**: `README_EN.md` (this file), UI via `?lang=en` parameter
- `config.json` help modal: DE/EN toggle
- Translations extensible via `config.json` → `"help.de"` / `"help.en"`

---

## 🐛 Known Issues

- [#1 Stale Verification Engine](https://github.com/huepfer13/3d-homelab-universe/issues/1)
- WebGL performance on very old GPUs: Canvas2D fallback active

---

## 📜 License

MIT — free to use, modify, and distribute.
