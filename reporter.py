import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
from config import GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS_FILE

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def generate_monthly_report():
    """
    Runs on 1st of every month at midnight:
    1. Reads all logs from Google Sheets
    2. Generates PDF report
    3. Uploads to Google Drive
    4. Clears old logs from Sheet
    """
    print("📊 Starting monthly report generation...")

    try:
        # Connect to Google Sheets
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_FILE, scopes=SCOPES
        )
        gs_client = gspread.authorize(creds)
        sheet = gs_client.open_by_key(GOOGLE_SHEET_ID).sheet1
        all_rows = sheet.get_all_values()

        if len(all_rows) <= 1:
            print("📊 No data to report")
            return

        headers = all_rows[0]
        data_rows = all_rows[1:]

        # Count categories
        categories = {}
        for row in data_rows:
            if len(row) >= 5:
                cat = row[4]
                categories[cat] = categories.get(cat, 0) + 1

        month_year = datetime.now().strftime("%B_%Y")
        filename = f"TeamSumit_{month_year}_Report.pdf"

        # Generate PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph(
            f"Team Sumit WhatsApp Agent Report — {datetime.now().strftime('%B %Y')}",
            styles['Title']
        ))
        elements.append(Spacer(1, 20))

        # Summary
        elements.append(Paragraph("Summary", styles['Heading2']))
        elements.append(Paragraph(
            f"Total Messages: {len(data_rows)}",
            styles['Normal']
        ))
        elements.append(Spacer(1, 10))

        # Category breakdown table
        elements.append(Paragraph("Category Breakdown", styles['Heading2']))
        cat_data = [["Category", "Count"]]
        for cat, count in categories.items():
            cat_data.append([cat, str(count)])

        cat_table = Table(cat_data, colWidths=[300, 100])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F3864')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.HexColor('#EEF3FF'), colors.white
            ]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(cat_table)
        elements.append(Spacer(1, 20))

        # Full message log table
        elements.append(Paragraph("Message Log", styles['Heading2']))
        table_data = [headers] + data_rows
        msg_table = Table(table_data, colWidths=[90, 80, 100, 180, 90])
        msg_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F3864')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.HexColor('#EEF3FF'), colors.white
            ]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(msg_table)

        doc.build(elements)
        print(f"✅ PDF generated: {filename}")

        # Upload to Google Drive
        drive_service = build('drive', 'v3', credentials=creds)
        file_metadata = {'name': filename}
        media = MediaFileUpload(filename, mimetype='application/pdf')
        uploaded = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"✅ Uploaded to Google Drive: {uploaded.get('id')}")

        # Clear old logs from Sheet (keep headers only)
        sheet.resize(rows=1)
        print("✅ Old logs cleared from Google Sheets")

        # Delete local PDF file
        os.remove(filename)
        print("✅ Monthly report complete!")

    except Exception as e:
        print(f"❌ Report generation failed: {e}")