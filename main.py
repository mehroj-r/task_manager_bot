import asyncio
import logging
import os
import sys
import dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types.bot_command import BotCommand

from handlers import register_all_handlers
from utils.bot_utils import set_descripton, set_commands, set_short_description

# Load .env variables
dotenv.load_dotenv()

TOKEN = os.getenv("BOT_API_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
register_all_handlers(dp)

async def main() -> None:

    # Create a bot instance
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await set_descripton(bot,"Task Manager Bot - Your personal task manager in Telegram. \n\n I'm here to help you stay organized and productive. \n\n Click /start to begin!")
    await set_short_description(bot, "Task Manager Bot - Your personal task manager in Telegram")
    await set_commands(bot, [
                BotCommand(command="/start", description="Start the bot"),
                BotCommand(command="/help", description="Get help"),
                BotCommand(command="/list_tasks", description="List all tasks"),
                BotCommand(command="/add_task", description="Add a new task"),
                BotCommand(command="/settings", description="Change settings"),
            ]
        )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())