from aiogram.fsm.state import State, StatesGroup

class TaskCreation(StatesGroup):

    waiting_for_task_title = State()
    waiting_for_task_description = State()
    waiting_for_task_due_date = State()

