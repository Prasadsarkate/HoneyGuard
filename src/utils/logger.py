import json, os, threading
from datetime import datetime
from rich.console import Console
from rich.table import Table
from .encryption import maybe_encrypt

_LOG_PATH = "logs/alerts.log"
_LOCK = threading.Lock()
_INITIALIZED = False
_SETTINGS = {"logging": {"format": "jsonl", "encrypted": False}}

console = Console()

# Try importing push_alert from Flask app
try:
    from app import push_alert
except ImportError:
    push_alert = None

def init_logging(settings=None):
    global _INITIALIZED, _SETTINGS
    if _INITIALIZED:
        return
    os.makedirs(os.path.dirname(_LOG_PATH), exist_ok=True)
    if settings:
        _SETTINGS = settings
    _INITIALIZED = True

def _format_log(level, message, extra=None):
    ts = datetime.utcnow().isoformat()
    if _SETTINGS.get("logging", {}).get("format") == "text":
        return f"[{ts}] {level}: {message}"
    payload = {"timestamp": ts, "level": level, "message": message}
    if isinstance(extra, dict):
        payload.update(extra)
    return json.dumps(payload, ensure_ascii=False)

def log_event(message, level="INFO", extra=None):
    # Console pretty print
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Timestamp", style="dim", width=20)
    table.add_column("Level", style="bold")
    table.add_column("Message", style="white")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table.add_row(ts, level, message)
    console.print(table)

    # File logging
    line = _format_log(level, message, extra)
    if _SETTINGS.get("logging", {}).get("encrypted"):
        line = maybe_encrypt(line)

    with _LOCK:
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    # 🔴 Emit to dashboard if push_alert available
    if push_alert:
        try:
            alert_data = json.loads(line) if line.strip().startswith("{") else {
                "timestamp": ts,
                "level": level,
                "message": message
            }
            push_alert(alert_data)
        except Exception as e:
            console.print(f"[red]Failed to push alert to dashboard: {e}[/red]")
