
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


def get_web_buttons(webapp_url, token):
    return bot.build_reply_markup([
        [Button.url(text='open', url=f'{webapp_url}?startapp={token}')],
    ])


def get_Q_buttons(users=None, add_empty_spaces=0):
    users = users or []

    buttons = [
        [Button.inline(text, data)]
        for text, data in users
    ]

    start_at = len(users)+1
    buttons += [
        [Button.inline(f'{start_at+i}. empty', str.encode(f'QE{start_at+i}'))]
        for i in range(add_empty_spaces)
    ]
    buttons += [[Button.inline('Quit', 'quit')]]
    return bot.build_reply_markup(buttons)


def rows_to_buttons(button_rows, tag=None, target=None):
    tag = tag or ''
    buttons = []
    for i, row in enumerate(button_rows):
        btn = row.buttons[0]
        if tag in btn.text and tag:
            buttons.append((f'{i+1}. empty', str.encode(f'QE{i+1}')))
        elif btn.data == target:
            buttons.append((f'{i+1}. {tag}', str.encode(f'QT{i+1}')))
        else:
            buttons.append((btn.text, btn.data))

    while buttons[-1][1][:2] == b'QE' and len(buttons) > 3:
        buttons = buttons[:-1]

    return buttons


async def get_member_ids(chat_id):
    members = await bot.get_participants(chat_id)
    members = tuple(filter(lambda m: not m.bot, members))
    return tuple(map(lambda m: m.id, members))


def get_user_tag(user):
    tag = user.first_name
    if user.username:
        tag = '@' + user.username

    return tag


def get_user_mention(_id, display_name='ඞ'):
    return f'[{display_name}](tg://user?id={_id})'


def groupby(iterable, chunk_size, filler=None):
    return zip_longest(
        *[iter(iterable)] * chunk_size,
        fillvalue=filler
    )


async def get_db(db_session: AsyncSession) -> AsyncSession:
    async with db_session() as session:
        return session
