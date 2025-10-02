import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import start, order, cart

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(order.router)
    dp.include_router(cart.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())