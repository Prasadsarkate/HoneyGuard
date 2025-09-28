# HoneyGuard Trap Tool

A deception-based security tool that plants realistic fake sensitive files (honeyfiles) and sends alerts
when they are accessed. Phase-4 ready: rotation, multi-channel alerts, encrypted logs, web UI, plugins,
cloud hooks, and a stub ML analyzer.

## Quickstart

```bash
python -m venv .venv && . .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

- Edit config in `config/settings.yaml` and `config/alerts.yaml`.
- Dashboard (optional): `python -m src.web_ui.app` and open http://127.0.0.1:5000

## Structure

See `docs/design_architecture.md` for module-level details.
