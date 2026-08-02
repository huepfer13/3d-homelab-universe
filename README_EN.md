# 🌌 3D Homelab Universe

> **Your entire homelab as a living, glowing sci-fi universe — at a glance.**
>
> 🚀 **[LIVE DEMO](https://huepfer13.github.io/3d-homelab-universe/)** — try it in your browser!

**3D Homelab Universe** transforms your servers, nodes, and containers into a breathtaking 3D galaxy. Watch live data packets with *additive-blending* glow, jump to individual containers with a click, and track task chains in the interactive event stream.

---

### 🚀 Quick Start

```bash
git clone https://github.com/huepfer13/3d-homelab-universe.git
cd 3d-homelab-universe
python3 -m http.server 8000
# Open http://localhost:8000/index.html
```

> 💡 **No cloning needed?** [Live demo on GitHub Pages](https://huepfer13.github.io/3d-homelab-universe/)

### ✨ Killer Features

* **🚀 Multi-Metric 3D Halos** — 3 independent rings per node: X=CPU, Y=RAM, Z=Disk I/O with real-time color (cyan→orange→red)
* **☄️ Data packets with trail history** — Comet tails follow movement direction + fade-in/out
* **🧠 Task & Trace Monitor** — Event stream with timestamps, color-coded status glow, expandable sub-tasks
* **🔗 Direct source linking** — Click opens issue tracker or document link
* **📂 Expandable hierarchy** — Accordion for galaxies, containers, pipelines
* **🕹️ OrbitControls** — Zoom, orbit, pan + center-universe button
* **⚙️ `config.json`** — External configuration with DE/EN help modal
* **🌍 Ring Metrics** — Horizontal=CPU, Vertical=RAM, Depth=Disk I/O with legend

### 📁 Structure

```
├── index.html          # Dashboard (self-contained)
├── config.json         # Configuration
├── test_universe.py    # Unit tests
├── SKILL.md            # AI Agent Integration
├── README.md / README_EN.md / CHANGELOG.md / LICENSE
```

### 🎥 Preview GIF

1. Record 5-10s (Peek/OBS/ShareX)
2. Save as `assets/preview.gif` and push
3. Appears automatically in the README!

### 🐛 Known Issues

- [#1 Stale Verification Engine](https://github.com/huepfer13/3d-homelab-universe/issues/1)

### 📜 License

MIT
