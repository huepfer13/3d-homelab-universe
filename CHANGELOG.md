# Changelog

## [v2.0.0] — 2026-08-03

### Added
- **Multi-Metric Halos**: 3 independent rings per object (X=CPU, Y=RAM, Z=Disk I/O)
  - Color transitions: cyan (idle) → orange (busy) → red (critical)
  - Per-ring pulsing with metric-specific frequency
  - Simulated metric drift for live data effect
  - Legend in HUD explaining ring/metric mapping
- **Canvas2D Fallback**: 25 animated pulsating dots when WebGL unavailable
- **GitHub Actions CI**: Tests, HTML validation, config check on every push
- **README_EN.md**: Full English documentation
- **5 Galaxy Layout**: Expanded from 3 to 5 galaxies (Alpha..Epsilon) with 25 containers
- **Ring Metrics Legend**: Visual guide for X/Y/Z → CPU/RAM/Disk mapping

### Changed
- Expanded from 3 galaxies / 11 containers → 5 galaxies / 25 containers
- Container IDs simplified: `a1..e5` instead of `node-a1..node-c3`
- Galaxy routes: 4 connections (alpha→beta→gamma→delta→epsilon)
- `fl()` updates simulation HUD immediately (was: after API timeout)
- Galaxy positions widened to -40..+40 on X-axis

### Fixed
- Removed broken `no-webgl` banner with escape issues
- `cl` TDZ bug causing Gg/Sg undefined on some browsers
- Accordion now shows all 5 galaxies and 25 containers
- `config.json` anonymized — zero project-specific names
- All project names removed from GitHub repo (BCHC, hostnames, CT-IDs)

### Removed
- All hardcoded project infrastructure names (Hermes, Paperless, Nextcloud, etc.)
- Three.js CDN dependency guard complexity (back to clean structure)
- Broken WebGL error banner with escape bugs

## [v1.1.0] — 2026-08-02

### Added
- OrbitControls with damping
- Multi-axis halo rings (XY, XZ, YZ planes)
- Click-to-center universe
- Crosshair HUD overlay
- Event stream with expandable sub-tasks
- Pipeline stages orbit animation
- Loop tubes between nodes

### Changed
- Packet labels projected 3D→2D with visibility culling
- Trail history for packet paths (comet tail effect)

## [v1.0.0] — 2026-07-27

- Initial release
- 3D spiderweb dashboard
- config.json-driven architecture
- Unit tests (test_universe.py)
