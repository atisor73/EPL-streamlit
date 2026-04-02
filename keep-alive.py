import requests

base = "https://atisor73-epl-dashboard.streamlit.app"

endpoints = [
    "/", 
    "/_stcore/health",
    "/_stcore/stream",
]

for ep in endpoints:
    try:
        r = requests.get(base + ep, timeout=30)
        print("GET", ep, r.status_code)
    except Exception as e:
        print("GET", ep, e)

# Try POST to wake
try:
    r = requests.post(base + "/_stcore/health", timeout=30)
    print("POST health", r.status_code)
except Exception as e:
    print("POST health", e)