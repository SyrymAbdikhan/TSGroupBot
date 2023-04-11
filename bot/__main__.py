
import logging
import asyncio

from bot.loader import bot

from bot import handlers


async def on_startup():
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
