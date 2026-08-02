# 🌌 3D Homelab Universe

> **Dein gesamtes Homelab als lebendiges, leuchtendes Sci-Fi-Universum – auf einen Blick.**

Vergiss trockene Tabellen und sterile Status-Listen. **3D Homelab Universe** verwandelt deine Server, Nodes und Container in eine atemberaubende 3D-Galaxie direkt auf deinem Kiosk-Display oder Browser!

Beobachte Live-Datenpakete, die als glühende Kometen mit echtem *Additive-Blending*-Glow durch den Raum flitzen, springe per Mausklick direkt in den Fokus einzelner Container oder verfolge komplexe Task-Ketten im interaktiven Event-Stream.

---

### ✨ Die Killer-Features

* **🚀 3D-Volumen-Halos:** Nodes und Container werden von dreidimensionalen XYZ-Energieringen eingefasst, die aus jedem Blickwinkel perfekt strahlen.
* **☄️ Lebendige Datenpakete:** Datenströme mit intelligentem Trail-History-Buffer und butterweichem Fade-In/Fade-Out beim Verlassen und Erreichen der Halos.
* **🧠 Interaktiver Task- & Trace-Monitor:** Event-Stream mit Start/End-Zeiten, farbcodiertem Status-Glühen (Grün/Erfolg, Rot/Fehler, Orange/Warnung) und aufklappbaren Folge-Nachrichten.
* **🔗 Direkte Quell-Verknüpfung:** Klick auf einen fertigen Auftrag öffnet die zugehörige externe Quelle (Gitea, Paperless) in einem neuen Tab.
* **📂 Aufklappbare Hierarchie-Legende:** Accordion-Menüs für blitzschnellen Zugriff auf alle Objekte im Universum.
* **🕹️ Volle 3D-Kontrolle:** Stufenloses Zoomen per Scrollrad, Orbit-Drehung per Mausklick, Pan-Verschiebung und "Center Universe"-Button.
* **⚙️ Externe Konfiguration (`config.json`):** Parameter von außen anpassbar, mit DE/EN-Hilfe im integrierten Modal-Fenster.

---

### 🚀 Quick Start

```bash
git clone https://github.com/huepfer13/3d-homelab-universe.git
cd 3d-homelab-universe
python3 -m http.server 8000
# Open http://localhost:8000/universe.html
```

### 🔧 Kiosk Mode

```bash
chromium --kiosk --no-first-run --disable-infobars http://localhost:8000/universe.html
```

### 🧪 Tests

```bash
python3 test_universe.py  # 11 unit tests
```

### 📁 Project Structure

```
3d-homelab-universe/
├── universe.html       # Main dashboard (self-contained)
├── config.json         # External configuration
├── test_universe.py    # 11 unit tests
├── SKILL.md            # Hermes Agent integration
├── README.md           # This file
├── CHANGELOG.md
└── LICENSE             # MIT
```

### 🎥 Create a Preview GIF

1. Record a 5-10s clip of the dashboard (Peek/OBS/ShareX)
2. Save as `assets/preview.gif`
3. Commit and push:
```bash
git add assets/preview.gif
git commit -m "docs: add live preview gif"
git push origin main
```
4. It appears automatically in this README!

### 🐛 Known Issues

- [#1 Stale Verification Engine](https://github.com/huepfer13/3d-homelab-universe/issues/1)

### 📜 License

MIT — see [LICENSE](LICENSE)
