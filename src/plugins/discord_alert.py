import yaml, requests

def discord_send(message: str, extra=None):
    with open("config/alerts.yaml", "r", encoding="utf-8") as f:
        url = yaml.safe_load(f).get("discord", {}).get("webhook_url", "")
    if not url:
        return
    content = message
    if extra:
        content += "\n" + "\n".join([f"{k}: {v}" for k, v in extra.items()])
    try:
        requests.post(url, json={"content": content}, timeout=5)
    except Exception:
        pass
