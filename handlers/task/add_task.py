from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from api.task import Task
from handlers.task.task_fsm import TaskCreation

router = Router()

@router.message(F.text == "/add_task")
async def start_task_creation(message: types.Message, state: FSMContext):
    await message.answer("Please enter the task title:")
    await state.set_state(TaskCreation.waiting_for_task_title)

@router.message(TaskCreation.waiting_for_task_title)
async def get_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Now enter the task description:")
    await state.set_state(TaskCreation.waiting_for_task_description)

@router.message(TaskCreation.waiting_for_task_description)
async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Enter the due date (YYYY-MM-DD):")
    await state.set_state(TaskCreation.waiting_for_task_due_date)

from datetime import datetime

@router.message(TaskCreation.waiting_for_task_due_date)
async def get_due_date(message: types.Message, state: FSMContext):
    due_date_str = message.text
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    except ValueError:
        await message.answer("❌ Invalid date format. Please use YYYY-MM-DD:")
        return

    data = await state.get_data()
    title = data["title"]
    description = data["description"]

    # Save it to database
    await Task(
        user=message.from_user,
        title=title,
        description=description,
        due_date=due_date.isoformat()
    ).add_task()

    await message.answer(
        f"✅ Task created:\n\n📌 *Title*: {title}\n📝 *Description*: {description}\n📅 *Due*: {due_date.date()}",
        parse_mode="Markdown"
    )

    await state.clear()




