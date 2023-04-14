
from telethon import TelegramClient

from bot.config import Config, load_config

config: Config = load_config()
bot = TelegramClient(
    config.bot.session_name,
    config.bot.api_id,
    config.bot.api_hash
)
bot.config = config.bot
bot.db_config = config.db
