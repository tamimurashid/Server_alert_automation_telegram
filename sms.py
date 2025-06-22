import requests
import base64
from config import BEAM_API_KEY, BEAM_API_SECRET, BEAM_SENDER_ID, ADMIN_PHONE_NUMBER

def send_sms_alert(message):
    url = "https://apisms.beem.africa/v1/send"
    credentials = f"{BEAM_API_KEY}:{BEAM_API_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }

    data = {
        "source_addr": BEAM_SENDER_ID,
        "encoding": "0",
        "schedule_time": "",
        "message": message,
        "recipients": [
            {"recipient_id": 1, "dest_addr": ADMIN_PHONE_NUMBER}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            print("[SMS] Alert sent successfully.")
        else:
            print(f"[SMS] Failed to send alert: {response.status_code} -> {response.text}")
    except Exception as e:
        print(f"[SMS] Exception sending alert: {e}")
