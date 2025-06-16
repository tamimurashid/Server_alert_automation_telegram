import time
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"[ERROR] Telegram send failed: {response.text}")
        else:
            print("[BOT] Message sent.")
    except Exception as e:
        print(f"[ERROR] Exception while sending Telegram message: {e}")

last_update_id = 0



def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={last_update_id + 1}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            updates = response.json()["result"]
            if updates:
                last_update_id = updates[-1]["update_id"]
            return updates
        else:
            print(f"[ERROR] Failed to get updates: {response.text}")
            return []
    except Exception as e:
        print(f"[ERROR] Exception while getting updates: {e}")
        return []
