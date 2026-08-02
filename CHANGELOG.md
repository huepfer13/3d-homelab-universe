# Changelog

## [1.1.0] - 2025-08-02
### Added
- **OrbitControls**: drag to rotate, scroll to zoom, right-drag to pan with damping
- **3D Multi-Axis Halos with AdditiveBlending**: Three orthogonal rings (XY, XZ, YZ) per galaxy and system — true 3D volume from any angle
- **Packet Fade-In/Out**: Opacity transition at halo entry/exit points
- **Accordion Hierarchy**: Expandable legend showing galaxies and systems, click to focus any node
- **Pipeline Badge**: HUD shows live CI/CD pipeline status with color coding
- **Event Log**: Streaming event stream with timestamps, color-coded by severity
- **Hover Tooltips**: Mouse-over nodes show metadata (type, radius, parent galaxy)
- **Connection Types**: active (solid cyan), ping (dim dashed), tube (curved red/orange arc)
- **Extended connection format**: Support `[from, to, type]` triples in config.json

### Changed
- Updated config.json with real 3-node homelab topology (11 systems, 12 packets)
- Universe position follows OrbitControls target for smoother click-to-center
- Improved camera damping behavior

### Fixed
- Test suite updated to support extended connection format

## [1.0.0] - 2024-08-02
### Added
- Initial release: universal config-driven 3D spiderweb dashboard
- Galaxy → Solar System → Planet hierarchical nesting
- 3D multi-axis ring halos (XY, XZ, YZ orthogonal rings)
- Color-coded animated packets with trails (ping-pong bounce)
- Click-to-center: shift universe to focus any object
- Pulsing load rings, permanent floating labels, crosshair
- try-catch safe animation loop
- Dual PointLights for even illumination
- Config-driven via `config.json`
- Live API integration (30s poll)
- 11 unit tests (config validation + HTML structure)
- SKILL.md for AI Agent integration
- MIT License
