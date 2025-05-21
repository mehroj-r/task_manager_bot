from functools import wraps

from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.methods import GetChatMember

CHANNEL_ID = "@task_manager_news"

def membership_required(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        is_member = await check_membership(message.from_user.id, message.bot)

        if not is_member:
            join_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Join Channel",
                            url=f"https://t.me/{CHANNEL_ID.strip('@')}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Check Membership",
                            callback_data="check_membership"
                        )
                    ]
                ]
            )
            return await message.answer("You must join our channel to use this bot.", reply_markup=join_button)

        return await handler(message, *args, **kwargs)
    return wrapper

async def check_membership(user_id: int, bot: Bot) -> bool:

    try:
        member = await GetChatMember(chat_id=CHANNEL_ID, user_id=user_id).as_(bot=bot)

        if member.status in ["member", "administrator", "creator"]:
            return True

        return False

    except Exception as e:
        print(f"Error checking membership: {e}")
        return False