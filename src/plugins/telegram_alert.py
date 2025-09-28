import yaml, requests

def telegram_send(message: str, extra=None):
    with open("config/alerts.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f).get("telegram", {})
    token = cfg.get("bot_token", "")
    chat_id = cfg.get("chat_id", "")
    if not token or not chat_id:
        return
    text = message
    if extra:
        text += "\n" + "\n".join([f"{k}: {v}" for k, v in extra.items()])
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=5)
    except Exception:
        pass
