import os
import json
import time
import traceback
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

CACHE_FILE = "last_state.txt"

def send_telegram(message):
    for attempt in range(3):
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"},
                timeout=10
            )
            return
        except Exception:
            time.sleep(2)

def blast_telegram(event):
    messages = [
        "🚨🚨🚨 <b>TICKETS ARE LIVE!!!</b> 🚨🚨🚨\nBRO DROP EVERYTHING RIGHT NOW! 🏃💨",
        "🎟🎟🎟 <b>GO BOOK NOW!!!</b> 🎟🎟🎟\n👉 https://tickets.tazkartifanzone.com",
        "⏰⏰⏰ <b>THEY WON'T LAST LONG!!!</b> ⏰⏰⏰\nEVERY SECOND COUNTS! 💥",
        "🔥🔥🔥 <b>STILL WAITING???</b> 🔥🔥🔥\nOPEN TELEGRAM NOW AND BOOK! 😤",
        f"🏆 <b>FINAL WARNING — FULL EVENT DATA:</b> 🏆\n\n"
        f"<pre>{json.dumps(event, indent=2)}</pre>\n\n"
        f"👉 https://tickets.tazkartifanzone.com\n\n"
        f"I stayed up for this. Don't waste it! 🎯",
    ]
    for msg in messages:
        send_telegram(msg)
        time.sleep(2)

def read_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return f.read().strip()
    except Exception:
        return "null"

def write_cache(value):
    try:
        with open(CACHE_FILE, "w") as f:
            f.write(value)
    except Exception:
        pass

def check_events():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        data = response.json()
        event = data.get("event")
        last_state = read_cache()

        if event is not None:
            event_hash = json.dumps(event, sort_keys=True)
            if last_state == "null":
                print("EVENT FOUND — blasting!")
                blast_telegram(event)
            else:
                print("Event already known — skipping blast.")
            write_cache(event_hash)
        else:
            print("No events yet.")
            write_cache("null")

    except Exception:
        tb = traceback.format_exc()
        print(tb)
        try:
            send_telegram(f"⚠️ GitHub Monitor error:\n<pre>{tb[-300:]}</pre>")
        except Exception:
            pass

if __name__ == "__main__":
    check_events()
