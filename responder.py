import requests
from config import WHATSAPP_TOKEN, PHONE_NUMBER_ID

async def send_whatsapp_reply(to: str, message: str):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"✅ Reply sent to {to}")
    else:
        print(f"❌ Failed to send reply: {response.text}")