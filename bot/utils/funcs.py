
from itertools import zip_longest

from telethon.tl.custom import Button
from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot


async def send_message(event, text, reply=False, **kwargs):
    if reply:
        msg = await event.reply(text, **kwargs)
    else:
        msg = await event.respond(text, **kwargs)
    return msg


def get_buttons(webapp_url, token):
    return bot.build_reply_markup([
        [Button.url('open', f'{webapp_url}?startapp={token}')],
    ])


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


async def get_db(db_session: AsyncSession) -> AsyncSession:
    async with db_session() as session:
        return session
