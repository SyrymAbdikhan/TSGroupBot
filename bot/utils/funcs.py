
import requests
from datetime import datetime
from itertools import zip_longest

from bot.loader import bot

offset = datetime.timedelta(hours=6)
tz = datetime.timezone(offset)


async def send_message(event, text, reply=False, file=None, keyboard=None):
    async with bot.action(event.chat_id, 'typing'):
        if reply:
            msg = await event.reply(text, file=file, buttons=keyboard)
        else:
            msg = await event.respond(text, file=file, buttons=keyboard)
        return msg


def get_moodle_events(token):
    moodle = bot.md_config
    payload = {
        "wstoken": token,
        "moodlewsrestformat": "json",
        "wsfunction": moodle.wsfunc,
        "timesortfrom": int(datetime.now(tz=tz).timestamp())
    }
    response = requests.get(moodle.url, payload)
    return response.json()['events']


async def get_member_ids(chat_id):
    members = await bot.get_participants(chat_id)
    members = tuple(filter(lambda m: not m.bot, members))
    return tuple(map(lambda m: m.id, members))


def make_tag(_id, display_name='ඞ'):
    return f'[{display_name}](tg://user?id={_id})'


def groupby(iterable, chunk_size, filler=None):
    return zip_longest(
        *[iter(iterable)] * chunk_size,
        fillvalue=filler
    )
