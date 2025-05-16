from .add_task import router as start_router
from .list_task import router as list_router

def setup_task_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(list_router)