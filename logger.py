import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS_FILE

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

async def log_message(sender: str, sender_name: str, message: str, category: str):
    """
    Logs every message to Google Sheets.
    Columns: Timestamp | Name | Number | Message | Category
    """
    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_FILE,
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sender_name,
            sender,
            message,
            category
        ]

        sheet.append_row(row)
        print(f"📝 Logged to Google Sheets")

    except Exception as e:
        print(f"❌ Logging failed: {e}")