def get_formatted_tasks_response(tasks) -> str:
    """
    Format the tasks for display with emoji numbering.
    """
    # Emoji numbers from 1-10
    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    response = "📝 <b>Tasks:</b>\n\n"
    for i, task in enumerate(tasks):
        # Use emoji numbers for 1-10, then fallback to regular numbers
        num_display = number_emojis[i] if i < len(number_emojis) else f"{i + 1}."

        response += (
            f"<b>{num_display} {task['title']}</b>\n"
            f"<u>Due</u>: {task['due_date']} | <u>ID</u>: {task['id']}\n"
        )
        # Only add description if it's not empty
        if task['description'].strip():
            response += f"<code>{task['description']}</code>\n"
        response += "\n"

    return response

def get_cursor(link) -> str:
    """
    Extracts cursor from the link.
    """

    tmp = link.split("?cursor=")

    if not link or len(tmp) != 2:
        raise Exception(f"Invalid link: {link}")

    return tmp[1]

def get_hash(data) -> str:
    """
    Extracts hash string from callback data
    """

    tmp = data.split("_")

    if not data or not len(tmp) >= 2:
        raise Exception(f"Invalid callback data: {data}")

    return tmp[-1]