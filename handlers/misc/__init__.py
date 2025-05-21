from .membership import router as membership_router

def setup_misc_handlers(dp):
    dp.include_router(membership_router)