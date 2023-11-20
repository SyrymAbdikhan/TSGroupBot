
from telethon import events

from bot.loader import bot
from bot.utils.funcs import (send_message, get_buttons,
                             get_member_ids, make_tag, groupby,
                             get_db)
from bot.utils.decorators import logger, is_group, type_action
from bot.db.models import ChatSettings


@bot.on(events.NewMessage(pattern=r'^/settoken'))
@logger
@is_group
@type_action
async def cmd_settoken(event):
    db_session = await get_db(bot.db)
    
    args = event.text.split()
    if len(args) < 2:
        await send_message(event, '❗️Too less arguments!\n/settoken <token>', reply=True)
        return await db_session.close()
    elif len(args) > 2:
        await send_message(event, '❗️Too many arguments!\n/settoken <token>', reply=True)
        return await db_session.close()
    
    token = args[1]
    chat = await ChatSettings.find(db_session, event.chat_id)
    if chat is None:
        chat = ChatSettings(chat_id=event.chat_id, moodle_token=token)
    else:
        chat.moodle_token = token
    
    await chat.save(db_session)
    
    await send_message(event, '✅ Successfully set token! New commands available now', reply=True)
    await db_session.close()


@bot.on(events.NewMessage(pattern=r'^(/c|@)all'))
@logger
@is_group
@type_action
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
@type_action
async def cmd_deadlines(event):
    db_session = await get_db(bot.db)
    chat = await ChatSettings.find(db_session, event.chat_id)
    await db_session.close()
    
    if chat is None:
        return await send_message(event, '❗️Please set token (/settoken) to use this command', reply=True)
    
    await send_message(
        event,
        'Here is the list of deadlines\nClick to Open 👇',
        reply=True,
        buttons=get_buttons(bot.config.webapp_url, chat.moodle_token)
    )
    