import time
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    escaped_text = escape_markdown(text)  # escape Markdown special chars
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": escaped_text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"[ERROR] Telegram send failed: {response.text}")
    else:
        print("[BOT] Message sent.")

last_update_id = 0

def escape_markdown(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    for ch in escape_chars:
        text = text.replace(ch, f"\\{ch}")
    return text


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
