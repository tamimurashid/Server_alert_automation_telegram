# 📡 Server Alert Automation Tool (Telegram + SMS)

This project is a cross-platform Python-based server and PC monitoring tool that alerts you via **Telegram** and **SMS (Beam Africa API)** when your machine or server goes down or experiences high usage (CPU, RAM, etc).

It works on **Linux, macOS, and even in virtual machines** (like Kali on VirtualBox) and can be deployed as a CLI utility for sysadmins, developers, or anyone managing remote/local servers.

---

## 🔧 Features

* ✅ Monitors CPU, RAM, disk usage, uptime, and OS
* ✅ Checks server (or public IP like 8.8.8.8) online status
* ✅ Telegram bot command interface (`/status`, `/ping`, `/setalert`...)
* ✅ Real-time alerts via Telegram and SMS (Beam Africa)
* ✅ User-defined alert thresholds
* ✅ Clean terminal output with optional `rich` formatting

---

## 🛠 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Server_alert_automation_telegram.git
cd Server_alert_automation_telegram
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you get warnings like `externally-managed-environment`, use a virtual environment as shown above.

---

## ⚙️ Configuration (Required)

Create a file named `config.py` inside the project root and paste the following **template** (⚠️ do not share your actual credentials):

```python
TELEGRAM_BOT_TOKEN = "<your-telegram-bot-token>"
TELEGRAM_CHAT_ID = "<your-chat-or-group-id>"
SERVER_TO_MONITOR = "<your-server-ip-or-hostname>"

BEAM_API_KEY = "<your-beam-api-key>"
BEAM_API_SECRET = "<your-beam-api-secret>"
BEAM_SENDER_ID = "<your-sender-id>"
ADMIN_PHONE_NUMBER = "<destination-phone-in-e164-format>"  # Example: 255712345678
```

### 🔑 Where to get the credentials:

* **Telegram Bot Token**: Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
* **Telegram Chat ID**: Use a bot like [@getidsbot](https://t.me/getidsbot) to find your chat or group ID
* **Beam Africa**: [Sign up here](https://beem.africa/) and get your API credentials

> 🔐 Keep this file secret. Do not commit it to version control.

---

## 🌍 VPN Warning (Telegram Access)

If you're in a region where Telegram is blocked (e.g. Tanzania), you must:

* Enable a **VPN** on your system to allow the Python script to access Telegram APIs.
* Alternatively, deploy the bot on a cloud VM in a region where Telegram is accessible.

---

## 🚀 Running the Bot

Once everything is set up:

```bash
python3 main.py
```

You’ll see:

```
[START] Monitoring started. Press Ctrl+C to stop.
[BOT] Listening for Telegram commands...
💻 PC STATUS
CPU: 15.4%
RAM: 65.2%
Disk: 24.5%
Uptime: 4h
OS: macOS-12.7.6-x86_64-i386-64bit
```

Use `/help` in the Telegram chat to list available commands.

---

## 📲 Telegram Bot Commands

| Command                        | Description                                           |
| ------------------------------ | ----------------------------------------------------- |
| `/status`                      | Show current PC status                                |
| `/server`                      | Check server online/offline                           |
| `/ping <ip>`                   | Ping any IP address                                   |
| `/setalert <resource> <value>` | Set CPU/RAM/temp threshold (e.g., `/setalert cpu 80`) |
| `/help`                        | Show help message                                     |

---

## 📦 Logging & Output

The tool logs all status updates, bot commands, and alerts to the terminal in real-time.

Optional enhancement: redirect logs to a file or send full logs to Telegram via a future command.

---

## 🔒 Disclaimer

This project is for educational and administrative purposes. Do not share your config details publicly. Always use environment variables or `.env` in production setups.

---

## 💡 Ideas to Improve

* Web dashboard with Flask + React
* Log history export (CSV/Excel)
* Alert pause/resume feature
* Multi-server monitoring

---

## ✨ Author

Tamimu Rashid a.k.a. Talian 🤖

Keep monitoring, stay alert.📡
