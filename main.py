import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import config
from handlers import router, run
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


async def scheduled_task(bot: Bot):
    chat_id = config.CHAT_ID
    await run(bot, chat_id)


def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_task, CronTrigger(hour=12), args=[bot])
    scheduler.start()


async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    setup_scheduler(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
