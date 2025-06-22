from telegram_bot import send_telegram_message, get_updates
from sms import send_sms_alert  # We
from monitor import get_system_status
from config import SERVER_TO_MONITOR
import subprocess
import threading
import json
import time
import re

last_status = {"online": True}

ALERT_FILE = "alert_thresholds.json"


# Load alert thresholds from file (if exists)
try:
    with open(ALERT_FILE, "r") as f:
        alert_thresholds = json.load(f)
except FileNotFoundError:
    # Default values
    alert_thresholds = {
        "cpu": 80,
        "ram": 80,
        "temp": 75
    }

# Function to save thresholds
def save_alert_thresholds():
    with open(ALERT_FILE, "w") as f:
        json.dump(alert_thresholds, f)


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
                text = message.get("text", "").strip()

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

                elif text == "/help":
                    help_msg = (
                        "🤖 *Available commands:*\n"
                        "/status - Show PC status\n"
                        "/server - Check if server is online\n"
                        "/ping <ip> - Ping an IP address\n"
                        "/setalert <resource> <value> - Set alert threshold (cpu, ram, temp)\n"
                        "/help - Show this message"
                    )
                    send_telegram_message(help_msg)

                elif text.startswith("/setalert"):
                    parts = text.split()
                    if len(parts) == 3:
                        resource, value = parts[1], parts[2]
                        if resource in alert_thresholds:
                            try:
                                val_int = int(value)
                                if 0 < val_int <= 100:
                                    alert_thresholds[resource] = val_int
                                    save_alert_thresholds()
                                    send_telegram_message(f"✅ Alert threshold for {resource} set to {val_int}%")
                                else:
                                    send_telegram_message("⚠️ Value must be between 1 and 100")
                            except ValueError:
                                send_telegram_message("⚠️ Invalid value, must be a number")
                        else:
                            send_telegram_message("⚠️ Invalid resource name. Use cpu, ram, or temp.")
                    else:
                        send_telegram_message("⚠️ Usage: /setalert <resource> <value>")

                elif text.startswith("/ping"):
                    parts = text.split()
                    if len(parts) == 2:
                        ip = parts[1]
                        if is_valid_ip(ip):
                            try:
                                response = subprocess.check_output(["ping", "-c", "2", ip], universal_newlines=True, timeout=5)
                                send_telegram_message(f"📡 Ping result for {ip}:\n{response}")
                            except subprocess.TimeoutExpired:
                                send_telegram_message(f"❌ Ping timed out for {ip}")
                            except Exception as e:
                                send_telegram_message(f"❌ Ping failed: {e}")
                        else:
                            send_telegram_message("⚠️ Invalid IP address.")
                    else:
                        send_telegram_message("⚠️ Usage: /ping <ip>")

                else:
                    send_telegram_message("⚠️ Unknown command. Type /help for the list of commands.")

            except Exception as e:
                print("[ERROR] Failed to handle update:", e)
        time.sleep(3)




def check_alerts():
    s = get_system_status()
    alerts = []
    
    if s["cpu"] > alert_thresholds["cpu"]:
        alerts.append(f"CPU usage critical: {s['cpu']}%")
    if s["ram"] > alert_thresholds["ram"]:
        alerts.append(f"RAM usage critical: {s['ram']}%")
    # If you have temp sensor:
    if "temp" in s and s["temp"] > alert_thresholds["temp"]:
        alerts.append(f"CPU Temperature critical: {s['temp']}°C")

    for alert in alerts:
        send_telegram_message(alert)
        send_sms_alert(alert)


def is_valid_ip(ip):
    pattern = re.compile(
        r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    )
    return bool(pattern.match(ip))

def escape_markdown(text):
    # Removed dot (.) and dash (-) because they don't need escaping in Telegram Markdown V2
    escape_chars = r'\_*[]()~`>#+=|{}!'  # no . and no -
    for ch in escape_chars:
        text = text.replace(ch, f"\\{ch}")
    return text

def check_alerts_loop():
    while True:
        check_alerts()
        time.sleep(300)  # check every 30 seconds (adjust as needed)




if __name__ == "__main__":
    print("[START] Monitoring started. Press Ctrl+C to stop.")
    threading.Thread(target=check_server_status, daemon=True).start()
    threading.Thread(target=listen_for_bot_commands, daemon=True).start()
    threading.Thread(target=check_alerts_loop, daemon=True).start()
    print_status_periodically()
