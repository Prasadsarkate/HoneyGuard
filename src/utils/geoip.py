# Stub: In production, add a MaxMind DB or an API call.
# Here we simply mark private ranges and unknowns.
from ipaddress import ip_address, ip_network

_PRIVATE = [
    ip_network('10.0.0.0/8'),
    ip_network('172.16.0.0/12'),
    ip_network('192.168.0.0/16'),
    ip_network('127.0.0.0/8'),
]

def lookup(ip: str):
    try:
        addr = ip_address(ip)
        for net in _PRIVATE:
            if addr in net:
                return {"ip": ip, "country": "Private", "city": "Private"}
        return {"ip": ip, "country": "Unknown", "city": "Unknown"}
    except Exception:
        return {"ip": ip, "country": "Invalid", "city": "Invalid"}
