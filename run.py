import os
import asyncio
import redis.asyncio as redis

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers.user_private import user_private_router
from app.aiohttp.aiohttp import update_redis_data

redis_client = redis.from_url("redis://redis:6379/0")

async def periodic_update(interval: int):
    while True:
        await update_redis_data()
        await asyncio.sleep(interval)

async def main():
    load_dotenv()

    bot = Bot(token=os.getenv("TG_TOKEN"))
    dp = Dispatcher()
    dp.include_router(user_private_router)

    interval = int(os.getenv("INTERVAL_UPDATE"))  # Интервал в секундах 
    asyncio.create_task(periodic_update(interval))
    
    try:
      await dp.start_polling(bot)
    except KeyboardInterrupt:
        await redis_client.aclose() 
        print("bot dont active")
    



if __name__ == "__main__":
    asyncio.run(main())
    