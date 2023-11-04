
from datetime import datetime, timedelta, timezone
from itertools import zip_longest

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot

offset = timedelta(hours=6)
tz = timezone(offset)
allowed_types = ('due', 'close')


async def send_message(event, text, reply=False, **kwargs):
    if reply:
        msg = await event.reply(text, **kwargs)
    else:
        msg = await event.respond(text, **kwargs)
    return msg


async def get_moodle_events(token):
    current_date = datetime.now(tz=tz)
    current_td = current_date - datetime(1970,1,1,tzinfo=tz) - offset
    timestamp_start = current_td.total_seconds()
    timestamp_end = (current_td + timedelta(days=60)).total_seconds()

    data = {'events': [], 'errors': []}
    next_date = current_date.replace(day=1)
    for _ in range(3):
        resp = await get_events(token, next_date.year, next_date.month)
        merge_dict_lists(data, resp)
        next_date = get_next_month(next_date)
    
    data['events'] = [event for event in data['events'] if event['eventtype'] in allowed_types and timestamp_start < event['timestart'] < timestamp_end]
    return data


async def get_events(token, year, month):
    moodle = bot.md_config
    payload = {
        'wstoken': token,
        'moodlewsrestformat': 'json',
        'wsfunction': 'core_calendar_get_calendar_monthly_view',
        'year': year,
        'month': month
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(moodle.url, params=payload) as resp:
                data = await resp.json()
        except Exception as e:
            return {'events': [], 'errors': [e.__class__.__name__]}
    
    events = [event for week in data.get('weeks', {}) for day in week.get('days', {}) for event in day.get('events', {})]
    errors = []
    if data.get('errorcode'):
        errors.append(data.get('errorcode'))

    return {'events': events, 'errors': errors}


def get_next_month(date):
    if date.month == 12:
        return datetime(date.year + 1, 1, 1)
    else:
        return datetime(date.year, date.month + 1, 1)


def merge_dict_lists(dct, merge_dct):
    for k in merge_dct.keys():
        dct[k] += merge_dct[k]


def format_time(dtime):
    if dtime.days < 0:
        return 'no time'

    units = []
    m, s = divmod(dtime.seconds, 60)
    h, m = divmod(m, 60)
    
    if dtime.days > 0:
        units.append(f'{dtime.days} days')

    if h > 0:
        units.append(f'{h} hr{"s" if h > 1 else ""}')

    if m > 0:
        units.append(f'{m} min{"s" if m > 1 else ""}')

    if s > 0 and dtime.days <= 0 and h == 0:
        units.append(f'{s} sec{"s" if s > 1 else ""}')

    text = ' '.join(units)
    if text:
        return text

    return 'no time'


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
