import yaml, requests

def slack_send(message: str, extra=None):
    with open("config/alerts.yaml", "r", encoding="utf-8") as f:
        url = yaml.safe_load(f).get("slack", {}).get("webhook_url", "")
    if not url:
        return
    text = message
    if extra:
        text += "\n" + "\n".join([f"{k}: {v}" for k, v in extra.items()])
    try:
        requests.post(url, json={"text": text}, timeout=5)
    except Exception:
        pass
