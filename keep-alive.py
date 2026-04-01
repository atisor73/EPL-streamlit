import requests
import time
url = "https://atisor73-epl-dashboard.streamlit.app/"
while True:
    try:
        requests.get(url)
        print("Pinged app")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(3600) # Ping every hour

