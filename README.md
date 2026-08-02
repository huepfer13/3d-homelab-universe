# 🌌 3D Homelab Universe

> **Dein gesamtes Homelab als lebendiges, leuchtendes Sci-Fi-Universum – auf einen Blick.**
>
> 🚀 **[LIVE DEMO](https://huepfer13.github.io/3d-homelab-universe/universe.html)** — direkt im Browser testen!

**3D Homelab Universe** verwandelt deine Server, Nodes und Container in eine atemberaubende 3D-Galaxie. Beobachte Live-Datenpakete mit *Additive-Blending*-Glow, springe per Klick zu einzelnen Containern und verfolge Task-Ketten im interaktiven Event-Stream.

---

### 🚀 Quick Start

```bash
git clone https://github.com/huepfer13/3d-homelab-universe.git
cd 3d-homelab-universe
python3 -m http.server 8000
# Open http://localhost:8000/universe.html
```

> 💡 **Kein Klonen noetig?** [Live-Demo auf GitHub Pages](https://huepfer13.github.io/3d-homelab-universe/universe.html)

### ✨ Killer-Features

* **🚀 3D-Volumen-Halos** — XYZ-Energieringe, die aus jedem Blickwinkel strahlen
* **☄️ Datenpakete mit Trail-History** — Kometen-Schweife folgen physikalisch der Bewegungsrichtung + Fade-In/Out
* **🧠 Task- & Trace-Monitor** — Event-Stream mit Zeitstempeln, farbcodiertem Status-Gluehen, aufklappbaren Sub-Tasks
* **🔗 Direkte Quell-Verknuepfung** — Klick oeffnet Gitea-Issue oder Paperless-Dokument
* **📂 Aufklappbare Hierarchie** — Accordion fuer Galaxien, Container, Pipelines
* **🕹️ OrbitControls** — Zoom, Orbit, Pan + Center-Universe-Button
* **⚙️ `config.json`** — externe Konfiguration mit DE/EN-Hilfe im Modal

### 📁 Struktur

```
├── universe.html       # Dashboard (self-contained)
├── config.json         # Konfiguration
├── test_universe.py    # 11 Unit-Tests
├── SKILL.md            # Hermes Agent Integration
├── README.md / CHANGELOG.md / LICENSE
```

### 🎥 Preview-GIF

1. 5-10s aufnehmen (Peek/OBS/ShareX)
2. Als `assets/preview.gif` speichern + pushen
3. Erscheint automatisch im README!

### 🐛 Known Issues

- [#1 Stale Verification Engine](https://github.com/huepfer13/3d-homelab-universe/issues/1)

### 📜 License

MIT
