from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
from config import VERIFY_TOKEN
from classifier import classify_message
from decision import handle_decision

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = None,
    hub_challenge: str = None,
    hub_verify_token: str = None
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("✅ Webhook verified by Meta!")
        return PlainTextResponse(content=hub_challenge)
    else:
        raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()

    try:
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" not in value:
            return {"status": "not a message, ignored"}

        message = value["messages"][0]
        sender_number = message["from"]
        message_type = message["type"]

        if message_type != "text":
            return {"status": "non-text message, ignored for now"}

        message_text = message["text"]["body"]

        print(f"📩 New message from {sender_number}: {message_text}")

        category = await classify_message(message_text)
        await handle_decision(
            sender=sender_number,
            message=message_text,
            category=category
        )

        return {"status": "processed"}

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "error", "detail": str(e)}