from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
import asyncio

from config import BOT_TOKEN
from handlers import menu, guess_number, knb, tic_tac_toe, donate, sms, web_app  # Импортируем новый модуль


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(knb.router)
    dp.include_router(menu.router)
    dp.include_router(guess_number.router)
    dp.include_router(tic_tac_toe.router)
    dp.include_router(donate.router)
    dp.include_router(sms.router)
    dp.include_router(web_app.router)

    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
