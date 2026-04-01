import requests
import time
# Replace with your actual app URL
url = "https://your-app-name.streamlit.app"
while True:
    try:
        requests.get(url)
        print("Pinged app")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(3600) # Ping every hour

