# 🏟️ EFZ Event Monitor — Direct API Version

Hits the **KNOT Technologies API** directly every 15 minutes.
No browser, no scraping — reads the real JSON data instantly.
Sends a **Telegram message** the moment events appear. 100% free on GitHub.

---

## ⚡ Setup (10 minutes)

### Step 1 — Create Telegram Bot
1. Open Telegram → search **@BotFather** → send `/newbot`
2. Copy the **token**: looks like `7123456789:AAFxxxxx`
3. Search **@userinfobot** → send any message → copy your **Chat ID**

### Step 2 — Create GitHub repo
1. Go to [github.com](https://github.com) → Sign Up (free)
2. **New repository** → name `efz-monitor` → **Private** → Create

### Step 3 — Upload files
Upload `monitor.py` to the root of the repo.

For `monitor.yml`, create the folder path:
- Click **Add file** → **Create new file**
- Type `.github/workflows/monitor.yml` as the filename
- Paste the contents → **Commit changes**

### Step 4 — Add Telegram secrets
Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| Name | Value |
|------|-------|
| `TELEGRAM_TOKEN` | Your bot token |
| `TELEGRAM_CHAT_ID` | Your chat ID |

### Step 5 — Test it
- Go to **Actions** tab → **EFZ Event Monitor** → **Run workflow**
- Check the logs — you'll see `✅ No events yet` or `🎉 EVENTS FOUND`

---

## ✅ Done!
Runs every 15 min forever for free. When events go live you get:

> 🎟 **New Event on Egyptian Fan Zone!**
> • Event Name Here
> أحداث جديدة متاحة الآن!
> 👉 Book Now
