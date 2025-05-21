from aiogram import types, Router
from aiogram.filters import CommandStart

from utils.decorators import membership_required

router = Router()


@router.message(CommandStart())
@membership_required
async def start_handler(message: types.Message):

    user = message.from_user

    # Greet the user
    await message.answer(
        f"👋 Hello, {user.first_name}!\n\n"
        "I'm your personal Task Manager Bot 📝.\n"
        "I can help you stay organized by tracking your tasks and projects right here in Telegram.\n\n"
        "Here are some things you can do:\n"
        "• /add_task – Create a new task\n"
        "• /list_tasks – View your tasks\n"
        "• /settings – Set your preferences\n\n"
        "Let's get productive! 🚀"
    )