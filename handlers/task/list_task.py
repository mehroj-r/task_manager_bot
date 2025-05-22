from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api.task import Task
from handlers.task.utils import get_formatted_tasks_response, get_cursor, get_hash
from utils.decorators import membership_required
from utils.redis_client import RedisClient
from .enum import TasksListMessageType

router = Router()

@router.message(F.text == "/list_tasks")
@membership_required
async def list_tasks_message_handler(message: types.Message):
    await handle_tasks_list(message=message, call_type=TasksListMessageType.MESSAGE)

@router.callback_query(F.data.startswith("tasks_nav_"))
@membership_required
async def list_tasks_callback_handler(callback: types.CallbackQuery):
    await handle_tasks_list(callback=callback, call_type=TasksListMessageType.CALLBACK_QUERY)

async def handle_tasks_list(message: types.Message=None, callback: types.CallbackQuery=None, call_type: TasksListMessageType=None):

    if not call_type:
        raise TypeError("Unknown call type")

    redis_client = RedisClient()
    user = message.from_user if message else callback.from_user

    cursor = None
    if call_type == TasksListMessageType.CALLBACK_QUERY:
        cursor = await redis_client.get_user_callback_data(user.id, get_hash(callback.data))

    # Get the tasks from the API
    tasks, next_page, previous_page = await Task(
        user=user,
        title=None,
        description=None,
        due_date=None
    ).get_tasks(cursor)

    # Check if tasks are empty
    if not tasks:

        if call_type == TasksListMessageType.MESSAGE:
            await message.answer("📭 You have no tasks yet. Use /add_task to create one!")
        else: # CALLBACK_QUERY
            raise Exception("No tasks found for the next page.")

        return

    # Format the tasks for display
    response = get_formatted_tasks_response(tasks)

    # Add inline pagination buttons
    builder = InlineKeyboardBuilder()
    button_count = 0 # Dynamic button count

    # Proccess Inline buttons: 'previous' and 'next'
    for i, page in enumerate([previous_page, next_page]):

        if not page:
            continue

        button_count += 1
        cursor = get_cursor(page)

        cb_hash = await redis_client.save_user_callback_data(user.id, cursor)
        cb_data = f"tasks_nav_{cb_hash}"

        if i == 0: # previous_page
            builder.button(text="⬅️ Previous", callback_data=cb_data)
        else: # next_page
            builder.button(text="Next ➡️", callback_data=cb_data)

    if button_count:
        builder.adjust(button_count) # Adjust the buttons to fit in two columns

    if call_type == TasksListMessageType.MESSAGE:
        await message.answer(response, parse_mode="HTML", reply_markup=builder.as_markup())
    else: # CALLBACK_QUERY
        await callback.message.edit_text(response, parse_mode="HTML", reply_markup=builder.as_markup())
