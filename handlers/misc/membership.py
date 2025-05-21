from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.user.start import start_handler
from utils.decorators import check_membership

router = Router()

@router.callback_query(F.data == "check_membership")
async def check_membership_callback(callback: CallbackQuery):

    # Check if the user is a member of the channel
    is_member = await check_membership(
        user_id=callback.from_user.id,
        bot=callback.bot
    )

    # If the user is not a member, send an alert
    if not is_member:
        return await callback.answer(
            text="You membership has not been verified. Please join our channel.",
            show_alert=True
        )

    # If the user is a member, proceed with the start handler
    await start_handler(callback.message)
    return await callback.message.delete()