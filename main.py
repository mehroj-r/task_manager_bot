import asyncio
import logging
import os
import sys
import dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import register_all_handlers

# Load .env variables
dotenv.load_dotenv()

TOKEN = os.getenv("BOT_API_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
register_all_handlers(dp)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())