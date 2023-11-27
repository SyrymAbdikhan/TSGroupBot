
from telethon import events

from bot.loader import bot
from bot.utils.funcs import (send_message, get_web_buttons, get_user_tag,
                             get_member_ids, get_user_mention, groupby,
                             get_db, get_Q_buttons, rows_to_buttons)
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
    mentions = [get_user_mention(_id) for _id in ids]

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
        buttons=get_web_buttons(bot.config.webapp_url, chat.moodle_token)
    )


@bot.on(events.NewMessage(pattern='^/newQ'))
@logger
@is_group
@type_action
async def create_Q_handler(event: events.NewMessage.Event):
    text = event.text.split(maxsplit=1)
    title = text[1] if len(text) > 1 else 'New Queue'

    await event.respond(f'{title}\n\nClick to Join the queue 👇', buttons=get_Q_buttons(add_empty_spaces=3))


@bot.on(events.CallbackQuery(pattern='QE[0-9]+'))
@logger
@is_group
async def join_QEn_callback(query: events.CallbackQuery.Event):
    tag = get_user_tag(query.sender)
    msg = await query.get_message()
    btn_rows = msg.reply_markup.rows[:-1]
    buttons = rows_to_buttons(btn_rows, tag, query.data)

    add = int(buttons[-1][1][:2] == b'QT')
    await query.edit(msg.message, buttons=get_Q_buttons(buttons, add_empty_spaces=add))



@bot.on(events.CallbackQuery(pattern='QT[0-9]+'))
@logger
@is_group
async def join_QTn_callback(query: events.CallbackQuery.Event):
    return await query.answer('This place is already taken')


@bot.on(events.CallbackQuery(data='quit'))
@logger
@is_group
async def quit_Q_callback(query: events.CallbackQuery.Event):
    tag = get_user_tag(query.sender)
    msg = await query.get_message()
    btn_rows = msg.reply_markup.rows[:-1]
    
    old_buttons = rows_to_buttons(btn_rows)
    buttons = rows_to_buttons(btn_rows, tag)
    if old_buttons == buttons:
        return await query.answer('You are not in the queue!')

    add = int(buttons[-1][1][:2] == b'QT')
    await query.edit(msg.message, buttons=get_Q_buttons(buttons, add_empty_spaces=add))
