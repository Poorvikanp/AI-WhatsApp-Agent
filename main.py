from fastapi import FastAPI, Request
from webhook import router as webhook_router
from classifier import classify_message
from decision import get_reply
from logger import log_message
from notifier import notify_sumit_sir, pending_alerts
from reporter import generate_monthly_report
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(
    title="Team Sumit AI WhatsApp Agent",
    version="1.0.0"
)

app.include_router(webhook_router)

# Monthly report scheduler
# Runs on 1st of every month at midnight automatically
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

    print(f"📩 New message from {sender_name}: {message}")

    # Step 1 - Classify
    category = await classify_message(message)
    print(f"🏷️ Category: {category}")

    # Step 2 - Log to Google Sheets
    await log_message(
        sender=sender,
        sender_name=sender_name,
        message=message,
        category=category
    )

    # Step 3 - Decision
    if category in ["IMPORTANT", "UNKNOWN"]:
        print(f"🚨 Escalating to Sumit Sir")
        await notify_sumit_sir(
            sender=sender,
            sender_name=sender_name,
            message=message,
            category=category
        )
        return {"escalate": True, "category": category}

    elif category == "SPAM":
        print(f"🗑️ Spam ignored")
        return {"reply": None, "category": category}

    else:
        reply = await get_reply(category)
        print(f"💬 Replying to {sender_name}")
        return {"reply": reply, "category": category}


@app.get("/pending-alerts")
async def get_pending_alerts():
    alerts = pending_alerts.copy()
    pending_alerts.clear()
    return {"alerts": alerts}


# Manual trigger for testing report generation
@app.get("/generate-report")
async def trigger_report():
    generate_monthly_report()
    return {"status": "Report generated and uploaded to Google Drive"}


@app.get("/")
def root():
    return {"status": "Team Sumit AI Agent is running"}