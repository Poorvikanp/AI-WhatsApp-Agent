

from fastapi import FastAPI, Request
from classifier import classify_message
from decision import get_reply
from logger import log_message
from notifier import notify_sumit_sir, pending_alerts
from reporter import generate_monthly_report
from apscheduler.schedulers.background import BackgroundScheduler

from memory import add_message

app = FastAPI(
    title="Team Sumit AI WhatsApp Agent",
    version="1.0.0"
)

# Monthly Report Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    generate_monthly_report,
    'cron',
    day=1,
    hour=0,
    minute=0
)
scheduler.start()


@app.post("/classify")
async def classify(request: Request):

    body = await request.json()

    sender = body.get("from")
    sender_name = body.get("sender_name", sender)
    message = body.get("message")

    print(f"\n📩 New message from {sender_name}")
    print(f"💬 {message}")

    # ----------------------------
    # Store User Message
    # ----------------------------
    add_message(sender, "User", message)

    # ----------------------------
    # AI Classification
    # ----------------------------
    category = await classify_message(sender, message)

    print(f"🏷️ Category : {category}")

    # ----------------------------
    # Google Sheets Logging
    # ----------------------------
    await log_message(
        sender=sender,
        sender_name=sender_name,
        message=message,
        category=category
    )

    # ----------------------------
    # IMPORTANT / UNKNOWN
    # ----------------------------
    if category in ["IMPORTANT", "UNKNOWN"]:

        print("🚨 Escalating to Sumit Sir")

        await notify_sumit_sir(
            sender=sender,
            sender_name=sender_name,
            message=message,
            category=category
        )

        return {
            "escalate": True,
            "category": category
        }

    # ----------------------------
    # SPAM
    # ----------------------------
    elif category == "SPAM":

        print("🗑️ Spam ignored")

        return {
            "reply": None,
            "category": category
        }

    # ----------------------------
    # Auto Reply
    # ----------------------------
    else:

        reply = await get_reply(category)

        print(f"💬 Replying to {sender_name}")

        # ----------------------------
        # Store Assistant Reply
        # ----------------------------
        add_message(sender, "Assistant", reply)

        return {
            "reply": reply,
            "category": category
        }


@app.get("/pending-alerts")
async def get_pending_alerts():

    alerts = pending_alerts.copy()
    pending_alerts.clear()

    return {
        "alerts": alerts
    }


@app.get("/generate-report")
async def trigger_report():

    generate_monthly_report()

    return {
        "status": "Report generated and uploaded to Google Drive"
    }


@app.get("/")
def root():

    return {
        "status": "Team Sumit AI Agent is running"
    }