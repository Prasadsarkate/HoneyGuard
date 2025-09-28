# Design & Architecture

- **Core**: file generation/rotation, monitoring, forensics, alert manager.
- **Utils**: logging (console + file), encryption (AES), geoip lookup.
- **Plugins**: alert channels + cloud storage hooks + SIEM webhook.
- **Web UI**: minimal Flask app to list and filter alerts.
- **ML**: basic analyzer to surface patterns (top IP, hourly histogram).

Key principles:
- Config-driven behaviour (YAML)
- Plugin interface for alerts/cloud
- JSONL log format (one JSON per line) + optional encryption
- Background scheduler for rotation using `schedule`
