import base64, json
from cryptography.fernet import Fernet

# Expect a base64 32-byte key in config/secrets.json (encryption_key)
_KEY = None

def set_key(key_b64: str):
    global _KEY
    if key_b64 and key_b64 != "REPLACE_WITH_32_BYTE_BASE64_KEY":
        _KEY = Fernet(key_b64.encode())

def maybe_encrypt(text: str) -> str:
    if _KEY is None:
        return text
    token = _KEY.encrypt(text.encode("utf-8"))
    return token.decode("utf-8")

def maybe_decrypt(token: str) -> str:
    if _KEY is None:
        return token
    try:
        plain = _KEY.decrypt(token.encode("utf-8"))
        return plain.decode("utf-8")
    except Exception:
        return token  # fallback
