
from os import getenv
from dataclasses import dataclass


@dataclass
class Bot:
    id: int
    token: str
    session_name: str
    api_id: str
    api_hash: str
    admin_id: int
    msg_size: int


@dataclass
class Config:
    bot: Bot


def load_config():
    return Config(
        bot=Bot(
            id=int(getenv('ADMIN_ID')),
            token=getenv('BOT_TOKEN'),
            session_name=getenv('SESSION_NAME'),
            api_id=getenv('API_ID'),
            api_hash=getenv('API_HASH'),
            admin_id=int(getenv('ADMIN_ID')),
            msg_size=int(getenv('MSG_SIZE'))
        )
    )
