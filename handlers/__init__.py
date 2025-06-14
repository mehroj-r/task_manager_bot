from .misc import setup_misc_handlers
from .task import setup_task_handlers
from .user import setup_user_handlers

def register_all_handlers(dp):
    setup_user_handlers(dp)
    setup_task_handlers(dp)
    setup_misc_handlers(dp)
