import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import bot.handlers.other as other_handlers
from bot import states
from bot.config import Config
from bot.database.base import register_models

logger = logging.getLogger(name=__name__)


async def _on_startup() -> None:
    await register_models()

    logger.info("Bot started")


async def main() -> None:
    bot = Bot(Config.TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(states.router)
    dp.include_router(other_handlers.router)

    dp.startup.register(_on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
