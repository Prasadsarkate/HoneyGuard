import argparse, json, yaml
from src.core.file_generator import generate_honeyfiles, rotation_scheduler, _rotate_once
from src.core.monitor import start_monitoring
from src.utils.logger import init_logging, log_event
from src.utils.encryption import set_key

def main():
    parser = argparse.ArgumentParser(description="HoneyGuard Tool CLI")
    parser.add_argument("--gen", action="store_true", help="Generate/ensure honeyguard now")
    parser.add_argument("--rotate", action="store_true", help="Force one rotation now")
    parser.add_argument("--monitor", action="store_true", help="Start monitoring (blocking)")
    parser.add_argument("--encrypt-logs", action="store_true", help="Enable encryption from secrets.json")
    args = parser.parse_args()

    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        settings = yaml.safe_load(f)

    init_logging(settings)

    if args.encrypt_logs:
        # Load key and enable encryption in settings
        try:
            from pathlib import Path
            import json as _json
            secrets = _json.loads(Path("config/secrets.json").read_text(encoding="utf-8"))
            set_key(secrets.get("encryption_key", ""))
            settings.setdefault("logging", {}).update({"encrypted": True})
            log_event("Log encryption enabled.", "INFO")
        except Exception as e:
            log_event(f"Failed to enable encryption: {e}", "WARN")

    if args.gen:
        generate_honeyfiles()

    if args.rotate:
        _rotate_once()

    if args.monitor:
        rotation_scheduler()
        start_monitoring()

if __name__ == "__main__":
    main()
