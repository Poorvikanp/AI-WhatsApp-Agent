# Team Sumit AI WhatsApp Agent 🤖

An autonomous AI Agent that manages WhatsApp messages for Sumit Sir — classifies incoming messages, auto-replies to routine queries, and alerts Sumit Sir only for urgent/important messages.

## What It Does

- Reads every incoming WhatsApp message in real time
- Uses Groq AI (llama-3.1-8b) to classify messages
- Auto-replies to internship, bootcamp, and seminar queries
- Silently ignores spam
- Alerts Sumit Sir on WhatsApp for urgent/unknown messages
- Logs everything to Google Sheets
- Auto-generates monthly PDF report and uploads to Google Drive

## Flow
Someone messages WhatsApp

↓

wa_client.js reads it

↓

FastAPI + Groq classifies it

↓

INTERNSHIP / BOOTCAMP / SEMINAR → Auto reply

SPAM → Ignored

IMPORTANT / UNKNOWN → Alert to Sumit Sir

↓

Logged to Google Sheets

## Project Structure

whatsapp_agent/

│

├── main.py           # FastAPI server — central brain

├── webhook.py        # Meta WhatsApp Cloud API webhook handler

├── classifier.py     # Groq AI message classification

├── decision.py       # Decision engine — what to do per category

├── responder.py      # Sends replies via Meta API

├── notifier.py       # Alerts Sumit Sir for urgent messages

├── logger.py         # Logs messages to Google Sheets

├── reporter.py       # Monthly PDF report generator

├── config.py         # API keys loader

├── wa_client.js      # WhatsApp Web connection (Node.js)

├── .env.example      # Environment variables template

└── requirements.txt  # Python dependencies


## Tech Stack

| Component | Tool | Cost |
|-----------|------|------|
| WhatsApp Connection | whatsapp-web.js | Free |
| Backend | FastAPI (Python) | Free |
| AI Classification | Groq API — llama-3.1-8b | Free |
| Message Logging | Google Sheets API | Free |
| Monthly Reports | ReportLab + Google Drive API | Free |
| Scheduler | APScheduler | Free |

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/team-sumit-whatsapp-agent.git
cd team-sumit-whatsapp-agent
```

### 2. Python setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Node setup
```bash
npm install
```

### 4. Environment variables
```bash
cp .env.example .env
# Fill in your actual keys in .env
```

### 5. Google Sheets setup
- Create a Google Sheet with headers: Timestamp | Name | Number | Message | Category
- Download service account credentials as `credentials.json`
- Share the sheet with the service account email

### 6. Run the agent

Terminal 1 — Start FastAPI:
```bash
uvicorn main:app --reload --port 8000
```

Terminal 2 — Start WhatsApp client:
```bash
node wa_client.js
```

Scan the QR code with WhatsApp → Agent is live!

## Message Categories

| Category | Action |
|----------|--------|
| INTERNSHIP_QUERY | Auto reply with internship form link |
| BOOTCAMP_QUERY | Auto reply with bootcamp details |
| SEMINAR_BOOKING | Auto reply asking for event details |
| SPAM | Silently ignored |
| IMPORTANT | Alert sent to Sumit Sir |
| UNKNOWN | Alert sent to Sumit Sir |

## Monthly Reports

Every 1st of the month at midnight:
- PDF report generated with message stats
- Uploaded to Google Drive automatically
- Google Sheets cleaned for next month

To trigger manually: `GET http://localhost:8000/generate-report`

## Built By

Poorvika NP & Ganeshwar — Suprazo Technologies, June 2026
