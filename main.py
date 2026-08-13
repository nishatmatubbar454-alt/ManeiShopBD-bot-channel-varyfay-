import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings
from database.database import db
from handlers import start, verify, referral, broadcast, menu

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # SQLite Persistent DB Initialization
    await db.init_db()

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Router Pipeline Engine
    dp.include_router(start.router)
    dp.include_router(verify.router)
    dp.include_router(referral.router)
    dp.include_router(broadcast.router)
    dp.include_router(menu.router)  # Global gate catches any unverified interaction

    logging.info("Bot execution started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
