# from groq import Groq
# from config import GROQ_API_KEY
# from memory import get_history

# # Initialize Groq client
# client = Groq(api_key=GROQ_API_KEY)

# # async def classify_message(message: str) -> str:
# async def classify_message(sender: str, message: str):
#     """
#     Takes an incoming WhatsApp message and classifies it
#     into one of these categories:
    
#     - INTERNSHIP_QUERY   → someone asking about internship
#     - BOOTCAMP_QUERY     → someone asking about bootcamp
#     - SEMINAR_BOOKING    → someone wants to book Sumit Sir for seminar
#     - IMPORTANT          → client, organizer, important person
#     - SPAM               → advertisement, random, irrelevant
#     - UNKNOWN            → agent cannot understand what they want
#     """

#     prompt = f"""
# You are an AI assistant for Sumit Sir, a tech entrepreneur and educator.
# Your job is to classify incoming WhatsApp messages into exactly ONE category.

# Categories:
# - INTERNSHIP_QUERY: Person asking about internship opportunities
# - BOOTCAMP_QUERY: Person asking about bootcamp details, fees, registration
# - SEMINAR_BOOKING: Person wants to invite Sumit Sir as speaker or judge
# - IMPORTANT: Message from a client, business partner, or organizer with urgent matter
# - SPAM: Advertisement, promotional message, irrelevant content
# - UNKNOWN: Cannot determine the intent clearly


# Message: "{message}"

# Reply with ONLY the category name. Nothing else. No explanation.
# """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         temperature=0.1,  # Low temperature = more consistent classification
#         max_tokens=20     # We only need one word back
#     )

#     # Extract the category from response
#     category = response.choices[0].message.content.strip().upper()

#     print(f"🏷️ Message classified as: {category}")

#     # Safety check - if Groq returns something unexpected, treat as UNKNOWN
#     valid_categories = [
#         "INTERNSHIP_QUERY",
#         "BOOTCAMP_QUERY", 
#         "SEMINAR_BOOKING",
#         "IMPORTANT",
#         "SPAM",
#         "UNKNOWN"
#     ]

#     if category not in valid_categories:
#         print(f"⚠️ Unexpected category '{category}' received, defaulting to UNKNOWN")
#         return "UNKNOWN"

#     return category

from groq import Groq
from config import GROQ_API_KEY
from memory import get_history

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


async def classify_message(sender: str, message: str) -> str:
    """
    Classifies incoming WhatsApp messages using
    previous conversation context.
    """

    # -----------------------------
    # Fetch previous conversation
    # -----------------------------
    history = get_history(sender)

    conversation = ""

    for chat in history:
        conversation += f"{chat['role']}: {chat['content']}\n"

    # -----------------------------
    # Build Prompt
    # -----------------------------
    prompt = f"""
You are an AI assistant for Sumit Sir, a tech entrepreneur and educator.

Your job is to classify incoming WhatsApp messages into exactly ONE category.

Categories:

- INTERNSHIP_QUERY
- BOOTCAMP_QUERY
- SEMINAR_BOOKING
- IMPORTANT
- SPAM
- UNKNOWN

Below is the previous conversation with this user.

Previous Conversation:

{conversation}

Current Message:

"{message}"

Only reply with ONE category.

Examples:

INTERNSHIP_QUERY
BOOTCAMP_QUERY
SEMINAR_BOOKING
IMPORTANT
SPAM
UNKNOWN

Do not explain.
Do not add extra text.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=20
    )

    category = response.choices[0].message.content.strip().upper()

    print(f"🏷️ Message classified as: {category}")

    valid_categories = [
        "INTERNSHIP_QUERY",
        "BOOTCAMP_QUERY",
        "SEMINAR_BOOKING",
        "IMPORTANT",
        "SPAM",
        "UNKNOWN"
    ]

    if category not in valid_categories:
        print("⚠️ Invalid category received.")
        return "UNKNOWN"

    return category