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
    print(f"Telegram sent: {response.status_code}")

def check_events():
    print(f"Checking API...")

    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        print(f"Status code: {response.status_code}")

        data = response.json()
        print(f"Response: {json.dumps(data)[:300]}")

        if data.get("success") == True and data.get("event") is not None:
            event = data.get("event", {})
            event_name = event.get("name") or event.get("title") or "New Event"
            event_date = event.get("date") or event.get("startDate") or ""

            print(f"EVENT FOUND: {event_name}")
            send_telegram(
                "New Event on Egyptian Fan Zone!\n\n"
                f"Event: {event_name}\n"
                f"Date: {event_date}\n\n"
                "Book Now: https://tickets.tazkartifanzone.com"
            )
        else:
            print("No events yet. Will check again in 15 minutes.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_events()
