# 🌌 3D Homelab Universe

> **Dein gesamtes Homelab als lebendiges, leuchtendes Sci-Fi-Universum – auf einen Blick.**
>
> 🚀 **[LIVE DEMO](https://huepfer13.github.io/3d-homelab-universe/)** — direkt im Browser testen!

**3D Homelab Universe** verwandelt deine Server, Nodes und Container in eine atemberaubende 3D-Galaxie mit **5 Galaxien à 5 Containern** (25 Systeme total). Jedes Objekt besitzt **3 unabhängige Multi-Metrik-Halos** (X=CPU, Y=RAM, Z=Disk I/O), die in Echtzeit ihre Farbe und Pulsation ändern. Datenpakete mit Trail-History fliegen zwischen den Nodes, der Event-Stream protokolliert alle Aktivitäten, und per Klick springst du direkt zu einzelnen Containern.

**Ohne WebGL?** Kein Problem — ein Canvas2D-Fallback zeichnet 25 animierte Punkte auf einem 5×5-Raster, sodass du immer visuelle Aktivität siehst.

---

## 🚀 Quick Start

```bash
git clone https://github.com/huepfer13/3d-homelab-universe.git
cd 3d-homelab-universe
python3 -m http.server 8000
# Öffne http://localhost:8000/index.html
```

> 💡 **Kein Klonen nötig?** [Live-Demo auf GitHub Pages](https://huepfer13.github.io/3d-homelab-universe/)

---

## ✨ Features

### 🪐 3D-Universum
- **5 Galaxien** (Alpha..Epsilon) auf X-Achse verteilt (-40..+40)
- **25 Container** (A1..A5, B1..B5, ..., E1..E5) mit eigenen Halos
- **OrbitControls**: Zoom, Orbit, Pan per Maus
- **Click-to-Center**: Klick auf Container/Galaxie zentriert das Universum
- **Double-Click auf Hintergrund**: Reset zum Zentrum (0,0,0)
- **Fadenkreuz-HUD**: Markiert permanent den Canvas-Mittelpunkt

### 📊 Multi-Metrik-Halos (NEU!)
Jeder Container und jede Galaxie hat **3 orthogonale Ringe**:
| Ring | Achse | Metrik | Farbe idle→busy→critical |
|------|-------|--------|--------------------------|
| ⬤ Horizontal | X | **CPU** | cyan → orange → rot |
| ⬤ Vertikal | Y | **RAM** | cyan → orange → rot |
| ⬤ Tiefe | Z | **Disk I/O** | cyan → orange → rot |

- Ringe pulsieren unabhängig mit metrik-spezifischer Frequenz
- Farbe wechselt graduell via `color.lerp()`
- Metriken driften zufällig (simulierte Live-Daten)
- **Legende** im HUD erklärt die Zuordnung

### ☄️ Datenpakete
- Fliegende Pakete mit **Trail-History** (Kometen-Schweif)
- **Fade-In/Out** an Start- und Endpunkten
- Farbcodiert nach Typ (Issue, Deploy, Error, Ping, Data)
- **Additive-Blending**-Glow für Sci-Fi-Look

### 🧠 Event-Stream
- Live-Log mit Zeitstempeln und **farbcodiertem Status**
- **Aufklappbare Sub-Tasks** (Parent→Child-Hierarchie)
- **Filter-Suche** im Event-Log
- Auto-Cleanup: Einträge werden nach 6h gelöscht
- Direkte **Quell-Verknüpfung**: Klick öffnet Issue/Link

### 📂 Hierarchie-Accordion
- **Aufklappbar**: Galaxien → Container → Pipelines
- **Focus-Node**: Klick zoomt zum ausgewählten Objekt
- Dynamisch aus `config.json` generiert

### 🎨 Canvas2D-Fallback
- Wenn WebGL nicht verfügbar ist (Headless-Browser, ältere GPUs):
  - 25 animierte, pulsierende Punkte auf 5×5-Raster
  - Galaxy-Farben (Blautöne)
  - Nahtloser Übergang: stoppt sobald WebGL läuft

### ⚙️ Konfiguration (`config.json`)
- Externe JSON-Datei definiert Galaxien, Container, Verbindungen, Pakete
- **DE/EN-Hilfe-Modal** mit Tastenkürzeln und Beschreibungen
- Farben, Positionen, Größen — alles anpassbar

### 🔧 CI/CD (GitHub Actions)
- Läuft **komplett auf GitHub** — entlastet Homelab-Systeme
- `test_universe.py` Unit-Tests bei jedem Push
- HTML-Validierung (DOCTYPE, Tags, Struktur)
- `config.json`-Validierung (5 Galaxien, 25 Systeme)

---

## 📁 Projektstruktur

```
├── index.html           # Dashboard (self-contained, 39 KB)
├── universe-3d.html     # 3D-only version
├── sim.html             # Minimal simulation
├── config.json          # 5 Galaxien, 25 Systeme, Verbindungen
├── test_universe.py     # Unit-Tests
├── SKILL.md             # AI-Agent-Integration
├── .github/workflows/   # CI/CD Pipeline
│   └── ci.yml
├── README.md            # Deutsche Doku (diese Datei)
├── README_EN.md         # English documentation
├── CHANGELOG.md
└── LICENSE (MIT)
```

---

## 🎮 Bedienung

| Aktion | Steuerung |
|--------|-----------|
| Orbit (drehen) | Linke Maustaste + ziehen |
| Zoom | Mausrad |
| Pan (verschieben) | Rechte Maustaste + ziehen |
| Objekt fokussieren | Klick auf Container/Galaxie |
| Zentrum reset | Doppelklick auf Hintergrund |
| Center-Button | ⌖ CENTER UNIVERSE im HUD |
| Accordion aufklappen | ▶ klicken |
| Event-Filter | Text in Filter-Box eingeben |

---

## 🌍 Lokalisierung

- **Deutsch**: `README.md` (diese Datei), UI-Texte im Dashboard
- **English**: `README_EN.md`, UI via `?lang=en` Parameter
- `config.json`-Hilfe-Modal: DE/EN-Umschaltung
- Übersetzungen erweiterbar via `config.json` → `"help.de"` / `"help.en"`

---

## 🐛 Known Issues

- [#1 Stale Verification Engine](https://github.com/huepfer13/3d-homelab-universe/issues/1)
- WebGL-Performance auf sehr alten GPUs: Canvas2D-Fallback aktiv

---

## 📜 License

MIT — frei verwendbar, modifizierbar, verteilbar.
