from telegram_bot import send_telegram_message, get_updates
from monitor import get_system_status
from config import SERVER_TO_MONITOR
import subprocess
import threading
import time

last_status = {"online": True}

def check_server_status():
    while True:
        try:
            response = subprocess.call(['ping', '-c', '1', SERVER_TO_MONITOR], stdout=subprocess.DEVNULL)
            online = (response == 0)
        except Exception:
            online = False

        if online != last_status["online"]:
            msg = "✅ *Server is back online!*" if online else "❌ *Server went down!*"
            send_telegram_message(msg)
            print(f"[Server] {msg}")

        last_status["online"] = online
        time.sleep(30)

def print_status_periodically():
    while True:
        s = get_system_status()
        print(
            f"\n💻 PC STATUS\n"
            f"CPU: {s['cpu']}%\n"
            f"RAM: {s['ram']}%\n"
            f"Disk: {s['disk']}%\n"
            f"Uptime: {int(s['uptime']//3600)}h\n"
            f"OS: {s['os']}\n"
        )
        time.sleep(60)

def listen_for_bot_commands():
    print("[BOT] Listening for Telegram commands...")
    while True:
        updates = get_updates()
        for update in updates:
            try:
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                print(f"[BOT] Command received: {text} from {chat_id}")

                if text == "/status":
                    s = get_system_status()
                    msg = (
                        f"💻 *PC Status:*\n"
                        f"CPU: {escape_markdown(str(s['cpu']))}%\n"
                        f"RAM: {escape_markdown(str(s['ram']))}%\n"
                        f"Disk: {escape_markdown(str(s['disk']))}%\n"
                        f"Uptime: {escape_markdown(str(int(s['uptime']//3600)))}h\n"
                        f"OS: {escape_markdown(s['os'])}"
                    )
                    send_telegram_message(msg)

                elif text == "/server":
                    msg = "✅ Server is Online" if last_status["online"] else "❌ Server is Offline"
                    send_telegram_message(msg)

            except Exception as e:
                print("[ERROR] Failed to handle update:", e)
        time.sleep(3)

def escape_markdown(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    for ch in escape_chars:
        text = text.replace(ch, f"\\{ch}")
    return text


if __name__ == "__main__":
    print("[START] Monitoring started. Press Ctrl+C to stop.")
    threading.Thread(target=check_server_status, daemon=True).start()
    threading.Thread(target=listen_for_bot_commands, daemon=True).start()
    print_status_periodically()
