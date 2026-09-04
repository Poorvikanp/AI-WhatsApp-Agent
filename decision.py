from logger import log_message

# ── Template replies for each category ───────────────────
replies = {
    "INTERNSHIP_QUERY": (
        "Hi! Thank you for reaching out to Sumit Sir. 🙏\n\n"
        "We are currently reviewing internship applications. "
        "Please fill out this form and we will get back to you shortly.\n"
        "Form link: [ADD YOUR FORM LINK HERE]\n\n"
        "For more updates follow us on Instagram and LinkedIn."
    ),
    "BOOTCAMP_QUERY": (
        "Hi! Thank you for your interest in our bootcamp! 🚀\n\n"
        "Here are the details:\n"
        "📅 Dates: [ADD DATES]\n"
        "💰 Fee: [ADD FEE]\n"
        "📍 Mode: [Online/Offline]\n\n"
        "Register here: [ADD REGISTRATION LINK]\n"
        "Feel free to ask if you have more questions!"
    ),
    "SEMINAR_BOOKING": (
        "Hi! Thank you for inviting Sumit Sir. 🎤\n\n"
        "Please share the following details so we can check availability:\n"
        "1. Event name and date\n"
        "2. Venue / Online platform\n"
        "3. Topic you want covered\n"
        "4. Expected audience size\n\n"
        "We will get back to you shortly!"
    ),
    "SPAM": None
}


async def get_reply(category: str) -> str:
    """
    Returns the template reply for a given category.
    Returns None for SPAM, IMPORTANT, UNKNOWN.
    """
    return replies.get(category)


async def handle_decision(sender: str, message: str, category: str):
    """
    Decision engine — called from main.py
    Decides what to do based on category:
    - ROUTINE → returns reply text
    - IMPORTANT/UNKNOWN → escalates
    - SPAM → ignores
    Logs everything to Google Sheets.
    """

    print(f"⚙️ Decision engine running for category: {category}")

    if category == "IMPORTANT" or category == "UNKNOWN":
        print(f"🚨 Escalating to Sumit Sir — category: {category}")

    elif category == "SPAM":
        print(f"🗑️ Spam detected, ignoring message from {sender}")

    else:
        reply_text = replies.get(category)
        if reply_text:
            print(f"💬 Sending auto reply for {category}")

    # Log everything
    await log_message(
        sender=sender,
        message=message,
        category=category
    )