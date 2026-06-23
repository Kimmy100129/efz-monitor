import os
import json
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# The real API endpoint found from browser DevTools
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
    print(f"Checking API: {API_URL}")

    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:500]}")

        if response.status_code != 200:
            print(f"API returned {response.status_code} — skipping")
            return

        data = response.json()

        # Check if there are any events in the response
        # The API returns an array or object with events
        has_events = False

        if isinstance(data, list) and len(data) > 0:
            has_events = True
            event_names = [e.get("name") or e.get("title") or "Event" for e in data[:3]]
        elif isinstance(data, dict):
            # Could be { events: [...] } or { data: [...] }
            events_list = data.get("events") or data.get("data") or data.get("items") or []
            if isinstance(events_list, list) and len(events_list) > 0:
                has_events = True
                event_names = [e.get("name") or e.get("title") or "Event" for e in events_list[:3]]
            elif data.get("name") or data.get("title"):
                # Single event object
                has_events = True
                event_names = [data.get("name") or data.get("title")]

        if has_events:
            print(f"🎉 EVENTS FOUND: {event_names}")
            events_text = "\n".join([f"• {name}" for name in event_names])
            send_telegram(
                "🎟 <b>New Event on Egyptian Fan Zone!</b>\n\n"
                f"{events_text}\n\n"
                "أحداث جديدة متاحة الآن!\n\n"
                "👉 <a href='https://tickets.tazkartifanzone.com'>احجز الآن / Book Now</a>"
            )
        else:
            print("✅ No events yet. Will check again next run.")

    except Exception as e:
        print(f"Error checking API: {e}")

if __name__ == "__main__":
    check_events()
