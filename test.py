import requests

TELEGRAM_TOKEN = '7277924109:AAGAEXRCJ7rxUDRqCSZMXo5pyQboZKJ3Fno'
CHAT_ID = '5000147537'

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': text
    }
    response = requests.post(url, data=data)
    print(response.json())

# Example use
send_telegram_message("🚀 Flask automation tool connected successfully!")
