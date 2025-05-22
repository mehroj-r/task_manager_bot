from functools import wraps

from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.methods import GetChatMember

CHANNEL_ID = "@task_manager_news"

def membership_required(handler):
    @wraps(handler)
    async def wrapper(message: Message=None, callback: CallbackQuery=None, *args, **kwargs):

        if message:
            is_member = await check_membership(message.from_user.id, message.bot)
        elif callback:
            is_member = await check_membership(callback.from_user.id, callback.bot)
        else:
            raise TypeError("Unknown call type")

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


        if message:
            return await handler(message, *args, **kwargs)

        if callback:
            return await handler(callback, *args, **kwargs)

        return None

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