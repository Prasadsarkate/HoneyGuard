import os, getpass, socket
from datetime import datetime

def collect_basic(event_path: str):
    # Best-effort local forensics
    info = {
        "path": event_path,
        "timestamp": datetime.utcnow().isoformat(),
        "user": getpass.getuser(),
        "hostname": socket.gethostname(),
        "pid": os.getpid(),
        # IP best-effort (local)
        "ip": _get_local_ip(),
    }
    return info

def _get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"
