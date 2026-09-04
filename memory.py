from collections import defaultdict

# -------------------------------
# Conversation Memory
# -------------------------------
# Stores conversation history for each WhatsApp user.
# Key   -> sender phone number
# Value -> list of conversation messages
# -------------------------------

conversation_memory = defaultdict(list)

# Maximum number of messages to remember
MAX_HISTORY = 10


def add_message(sender: str, role: str, content: str):
    """
    Add a message to the conversation history.

    sender -> WhatsApp ID
    role   -> "User" or "Assistant"
    content -> Actual message text
    """

    conversation_memory[sender].append({
        "role": role,
        "content": content
    })

    # Keep only the latest MAX_HISTORY messages
    if len(conversation_memory[sender]) > MAX_HISTORY:
        conversation_memory[sender] = conversation_memory[sender][-MAX_HISTORY:]


def get_history(sender: str):
    """
    Returns the conversation history of a user.
    """

    return conversation_memory.get(sender, [])


def clear_history(sender: str):
    """
    Clears conversation history of a user.
    """

    conversation_memory[sender] = []


def print_history(sender: str):
    """
    Debug function.
    Prints conversation history in terminal.
    """

    print("\n==============================")
    print(f"Conversation History : {sender}")
    print("==============================")

    history = get_history(sender)

    if not history:
        print("No conversation found.")
    else:
        for msg in history:
            print(f"{msg['role']}: {msg['content']}")

    print("==============================\n")