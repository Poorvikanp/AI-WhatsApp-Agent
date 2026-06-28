# Global list to store pending alerts
pending_alerts = []

async def notify_sumit_sir(sender: str, sender_name: str, message: str, category: str):
    """
    Queues a WhatsApp alert to Sumit Sir.
    wa_client.js polls /pending-alerts every 5 seconds and sends them.
    """

    # Replace with Sumit Sir's actual number
    SUMIT_SIR_NUMBER = "91XXXXXXXXXX@c.us"

    alert_message = (
        f"🚨 URGENT MESSAGE\n\n"
        f"From: {sender_name}\n"
        f"Number: +{sender.replace('@c.us', '').replace('@lid', '')}\n"
        f"Category: {category}\n\n"
        f"Message:\n'{message}'\n\n"
        f"Please reply manually."
    )

    pending_alerts.append({
        "to": SUMIT_SIR_NUMBER,
        "message": alert_message
    })

    print(f"🚨 Alert queued for Sumit Sir")