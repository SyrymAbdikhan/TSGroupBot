
import logging
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.loader import bot
from bot.config import DB
from bot.db.base import Base

from bot import handlers


async def get_async_sessionmaker(db: DB):
    engine = create_async_engine(
        f'postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}',
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )


async def on_startup():
    bot.db = await get_async_sessionmaker(bot.db_config)
    logging.info("Bot started!")


async def on_shutdown():
    logging.info("Bot shutdown!")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    logging.info("Initializing bot")

    try:
        await on_startup()
        await bot.start(bot_token=bot.config.token)
        await bot.run_until_disconnected()
    finally:
        await on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
