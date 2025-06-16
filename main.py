import subprocess
import time
import threading
from monitor import get_system_status
from telegram_bot import send_telegram_message
from config import SERVER_TO_MONITOR

last_status = {"online": True}

def check_server_status():
    while True:
        try:
            response = subprocess.call(['ping', '-c', '1', SERVER_TO_MONITOR], stdout=subprocess.DEVNULL)
            online = (response == 0)
        except Exception:
            online = False

        if online != last_status["online"]:
            if online:
                send_telegram_message("✅ *Server is back online!*")
                print("[INFO] Server is online")
            else:
                send_telegram_message("❌ *Server went down!*")
                print("[ERROR] Server is offline!")

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

if __name__ == "__main__":
    print("[START] Monitoring started. Press Ctrl+C to stop.")
    threading.Thread(target=check_server_status, daemon=True).start()
    print_status_periodically()
