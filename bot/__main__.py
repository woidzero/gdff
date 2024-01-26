import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import bot.handlers.other as other_handlers
import bot.handlers.user as user_handlers
from bot import states
from bot.database.base import register_models
from bot.settings import Settings

logger = logging.getLogger(name=__name__)


async def _on_startup() -> None:
    await register_models()

    logger.info("Bot started")


async def main() -> None:
    settings = Settings()

    bot = Bot(settings.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(other_handlers.router)  # must be first router to include
    dp.include_router(states.router)
    dp.include_router(user_handlers.router)

    dp.startup.register(_on_startup)

    await bot.delete_webhook(drop_pending_updates=settings.drop_pending_updates)
    if settings.drop_pending_updates:
        logger.info("Updates skipped successfully")

    await dp.start_polling(bot, settings=settings)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
