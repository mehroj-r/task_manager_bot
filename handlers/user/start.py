from aiogram import types, Router
from aiogram.filters import CommandStart

from api.auth import Auth
from utils.redis_client import RedisClient

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):

    user = message.from_user
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

    # Check if the token is valid
    token = await RedisClient().get_user_token(user.id)

    if not token:

        # Otherwise get new token
        await Auth(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code
        ).get_token()

