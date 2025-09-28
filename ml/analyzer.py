# Simple analyzer example: parse logs and compute top IPs, top files, hourly hits.
import json, os
from collections import Counter, defaultdict
from src.utils.encryption import maybe_decrypt

LOG_PATH = "logs/alerts.log"

def analyze():
    if not os.path.exists(LOG_PATH):
        return {"top_ips": [], "top_files": [], "by_hour": {}}

    ips = Counter()
    files = Counter()
    by_hour = defaultdict(int)

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(maybe_decrypt(line))
                ip = obj.get("ip") or obj.get("extra", {}).get("ip")
                path = obj.get("path") or obj.get("extra", {}).get("path")
                ts = obj.get("ts", "")
                if ip:
                    ips[ip] += 1
                if path:
                    files[path] += 1
                # hour bucket
                if len(ts) >= 13:
                    hour = ts[11:13]
                    by_hour[hour] += 1
            except Exception:
                continue

    return {
        "top_ips": ips.most_common(5),
        "top_files": files.most_common(5),
        "by_hour": dict(sorted(by_hour.items())),
    }

if __name__ == "__main__":
    print(analyze())
