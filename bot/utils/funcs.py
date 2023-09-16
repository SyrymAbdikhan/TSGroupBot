
import requests
from datetime import datetime, timedelta, timezone
from itertools import zip_longest

from sqlalchemy.ext.asyncio import AsyncSession

from bot.loader import bot

offset = timedelta(hours=6)
tz = timezone(offset)


async def send_message(event, text, reply=False, file=None, keyboard=None):
    async with bot.action(event.chat_id, 'typing'):
        if reply:
            msg = await event.reply(text, file=file, buttons=keyboard)
        else:
            msg = await event.respond(text, file=file, buttons=keyboard)
        return msg


def get_moodle_events(token):
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    shifted_date = get_next_month(current_date.replace(day=1))
    timestamp = (current_date - datetime(1970,1,1) - offset).total_seconds()

    events = []
    events += get_events(token, current_date.year, current_date.month)
    events += get_events(token, shifted_date.year, shifted_date.month)
    
    events = list(filter(lambda x: x['eventtype'] == 'due', events))
    events = list(filter(lambda x: x['timestart'] > timestamp, events))
    
    return events


def get_events(token, year, month):
    moodle = bot.md_config
    payload = {
        'wstoken': token,
        'moodlewsrestformat': 'json',
        'wsfunction': 'core_calendar_get_calendar_monthly_view',
        'year': year,
        'month': month
    }

    response = requests.get(moodle.url, payload)
    data = response.json()
    events = [event for week in data['weeks'] for day in week['days'] for event in day['events']]
        
    return events


def get_next_month(date):
    if date.month == 12:
        return datetime(date.year + 1, 1, 1)
    else:
        return datetime(date.year, date.month + 1, 1)


def get_largest_unit(dtime):
    if dtime.days > 0:
        return f'{dtime.days} days'

    if dtime.days < 0:
        return 'no time'

    m, s = divmod(dtime.seconds, 60)
    h, m = divmod(m, 60)

    if h > 0:
        return f'{h} hour{"s" if h > 1 else ""}'

    if m > 0:
        return f'{m} minute{"s" if m > 1 else ""}'

    if s > 0:
        return f'{s} second{"s" if s > 1 else ""}'

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
