import os
import json
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

API_URL = "https://api.knottech.ai/api/business/upcoming-event/6a14b61cc54f9f013f8c7fe7"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "ngrok-skip-browser-warning": "any",
    "origin": "https://tickets.tazkartifanzone.com",
    "referer": "https://tickets.tazkartifanzone.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

def send_telegram(message):
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
    )
    print(f"Telegram status: {response.status_code}")
    print(f"Telegram response: {response.text}")

def check_events():
    print("Checking API...")

    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        print(f"Status code: {response.status_code}")

        data = response.json()
        print(f"Response: {json.dumps(data)[:300]}")

        event = data.get("event")

        if event is None:
            print("No events yet. Will check again in 15 minutes.")
            send_telegram("EFZ Monitor ✅ Checked — No events yet.")
        else:
            print(f"EVENT FOUND: {event}")
            send_telegram(
                f"🎟 New Event on Egyptian Fan Zone!\n\n"
                f"{json.dumps(event, indent=2)}\n\n"
                f"Book Now: https://tickets.tazkartifanzone.com"
            )

    except Exception as e:
        print(f"Error: {e}")
        send_telegram(f"⚠️ EFZ Monitor error: {e}")

if __name__ == "__main__":
    check_events()
