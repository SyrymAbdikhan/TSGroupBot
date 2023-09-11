
from datetime import datetime

from telethon import events

from bot.loader import bot
from bot.utils.funcs import (send_message, get_moodle_events,
                             get_member_ids, make_tag, groupby, tz)
from bot.utils.decorators import logger, is_group


@bot.on(events.NewMessage(pattern=r'^(/|@)all'))
@logger
@is_group
async def cmd_all(event):
    ids = await get_member_ids(event.chat_id)
    mentions = [make_tag(_id) for _id in ids]

    texts = groupby(mentions, bot.config.msg_size, '')
    texts = list(map(lambda el: ''.join(el), texts))
    texts[0] = 'Calling mates ඞ...\n\n' + texts[0]

    for text in texts:
        await send_message(event, text)


@bot.on(events.NewMessage(pattern=r'^/deadlines'))
@logger
@is_group
async def cmd_deadlines(event):
    moodle_events = get_moodle_events(bot.md_config.token)
    
    text = '🥳 No Deadlines for now'
    if moodle_events:
        text = '💀 All deadlines:\n\n'
    
    for i, moodle_event in enumerate(moodle_events):
        dtime = datetime.fromtimestamp(int(moodle_event['timestart']), tz=tz)
        text += f'{i+1}. 📚 {moodle_event["course"]["fullname"]}\n' \
                f'📝 {moodle_event["name"]}\n' \
                f'⏰ {dtime.strftime("%B %d, %H:%M:%S")}\n\n'
    
    await send_message(event, text, reply=True)
    