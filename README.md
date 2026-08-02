# 3D Spiderweb Universe

Universal Three.js dashboard — galaxies, solar systems, planets, and animated data packets. Fully config-driven via `config.json`.

## Features
- 🌌 Hierarchical galaxy → solar system → planet nesting
- 🎯 Click-to-center: click any object to focus the universe
- 🔮 Color-coded data packets with trails (issue/deploy/error/ping/data)
- 💫 Oscillating rotation, pulsing load rings
- 🔍 LineLoop halos, permanent floating labels
- 📄 Universal: drop your own `config.json`, no code changes needed

## Quick Start
```bash
python3 -m http.server 8000
# Open http://localhost:8000/universe.html
```

## Configuration
Edit `config.json` — see the included sample for structure:
- `galaxies`: top-level nodes (servers/clusters)
- `systems`: child nodes inside galaxies (services/containers)
- `connections`: links between systems
- `packets`: animated data flows

## License
MIT
