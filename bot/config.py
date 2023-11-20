
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
    webapp_url: str


@dataclass
class Moodle:
    token: str
    url: str
    wsfunc: str


@dataclass
class DB:
    host: str
    port: int
    name: str
    user: str
    password: str


@dataclass
class Config:
    bot: Bot
    moodle: Moodle
    db: DB


def load_config():
    return Config(
        bot=Bot(
            id=int(getenv('BOT_ID')),
            token=getenv('BOT_TOKEN'),
            session_name=getenv('SESSION_NAME'),
            api_id=getenv('API_ID'),
            api_hash=getenv('API_HASH'),
            admin_id=int(getenv('ADMIN_ID')),
            msg_size=int(getenv('MSG_SIZE')),
            webapp_url=getenv('WEBAPPURL')
        ),
        moodle=Moodle(
            token=getenv('MOODLE_TOKEN'),
            url=getenv('MOODLE_URL'),
            wsfunc=getenv('WSFUNCTION')
        ),
        db=DB(
            host=getenv('DB_HOST'),
            port=int(getenv('DB_PORT')),
            name=getenv('DB_NAME'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASS')
        )
    )
