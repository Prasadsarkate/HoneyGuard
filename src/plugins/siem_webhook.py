import requests

def send_webhook(message: str, extra: dict | None, url: str):
    if not url:
        return
    payload = {"message": message, "extra": extra or {}}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass
