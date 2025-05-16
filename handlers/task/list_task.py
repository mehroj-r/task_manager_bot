from aiogram import types, Router, F
from api.task import Task

router = Router()

@router.message(F.text == "/list_tasks")
async def list_tasks_handler(message: types.Message):

    tasks = await Task(
        user=message.from_user,
        title=None,
        description=None,
        due_date=None
    ).get_tasks()

    if not tasks:
        await message.answer("📭 You have no tasks yet. Use /add_task to create one!")
        return

    response = "📝 *Your Tasks:*\n\n"
    for i, task in enumerate(tasks, start=1):
        response += (
            f"*{i}. {task['title']}*\n"
            f"📝 {task['description']}\n"
            f"📅 Due: `{task['due_date']}`\n"
            f"🆔 ID: `{task['id']}`\n\n"
        )

    await message.answer(response, parse_mode="Markdown")
