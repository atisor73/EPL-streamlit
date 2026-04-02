import requests

urls = [
    "https://atisor73-epl-dashboard.streamlit.app/",
    "https://atisor73-epl-dashboard.streamlit.app/_stcore/health"
]

for url in urls:
    try:
        r = requests.get(url, timeout=30)
        print(url, r.status_code)
    except Exception as e:
        print(url, e)
