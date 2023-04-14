
import logging
import re

from telethon import events, Button
from bot.db.models import Formatter

from bot.loader import bot
from bot.utils.funcs import *
from bot.utils.decorators import logger


async def get_formatter(chat_id):
    async with bot.db() as db_session:
        formatter = await Formatter.find(db_session, chat_id)
        if formatter is None:
            formatter = Formatter(chat_id=chat_id)
            await formatter.save(db_session)
    
    return formatter


async def get_kb(chat_id):
    formatter = await get_formatter(chat_id)
    return [
        Button.inline(
            f'Auto format: {"✅" if formatter.auto_format else "❌"}',
            'auto_format'
        ),
        Button.inline(
            f'Auto delete: {"✅" if formatter.auto_delete else "❌"}',
            'auto_delete'
        )
    ]


@bot.on(events.NewMessage(pattern=r'/start'))
@logger
async def cmd_start(event):
    await send_message(event, 'Hello! I\'m assistant bot specially made for TS MF group.'
                              'Type /help for more information')


@bot.on(events.NewMessage(pattern=r'/help'))
@logger
async def cmd_help(event):
    await send_message(event, 'Here is the bot commands:\n\n'
                              '/all - mention all members of the group\n'
                              '/formatter - deadline formatter settings\n'
                              '/help - more information about bot\n\n'
                              'Developer contacts: @Honey_Niisan')


@bot.on(events.NewMessage(pattern=r'🔥 Ближайшие дедлайны на 60 дней:'))
@logger
async def auto_formatter(event):
    formatter = await get_formatter(event.chat_id)
    if not formatter.auto_format:
        return

    text = event.raw_text
    new_text = re.sub("\n\d+\. ", "\n\n===========\n", text)
    new_text = re.sub(" \| ", "\n", new_text)

    await send_message(event, new_text)
    
    if formatter.auto_delete:
        await event.delete()


@bot.on(events.NewMessage(pattern=r'/formatter'))
@logger
async def cmd_formatter_settings(event):
    keyboard = await get_kb(event.chat_id)
    await send_message(event, '⚙️ settings', keyboard=keyboard)


@bot.on(events.CallbackQuery)
@logger
async def formatter_settings_handler(event):
    data = bytes.decode(event.data, 'utf-8')

    formatter = await get_formatter(event.chat_id)
    async with bot.db() as db_session:
        if data == 'auto_format':
            await formatter.update(
                db_session,
                auto_format=not formatter.auto_format
            )
        elif data == 'auto_delete':
            await formatter.update(
                db_session,
                auto_delete=not formatter.auto_delete
            )

    keyboard = await get_kb(event.chat_id)
    await bot.edit_message(event.chat_id, event.original_update.msg_id, buttons=keyboard)


@bot.on(events.ChatAction())
@logger
async def chat_action(event):
    if event.user_joined or event.user_added:
        await send_message(event, 'Welcome to the group!')
    elif event.user_left or event.user_kicked:
        await send_message(event, 'R.I.P 💔')


@bot.on(events.NewMessage(pattern=r'/all'))
@bot.on(events.NewMessage(pattern=r'^@all$'))
@logger
async def cmd_all(event):
    if event.is_private:
        return await send_message(event, 'Add me to the group to use this command', reply=True)

    ids = await get_member_ids(event.chat_id)
    mentions = [make_tag(_id) for _id in ids]

    texts = groupby(mentions, bot.config.msg_size, '')
    texts = list(map(lambda el: ''.join(el), texts))
    texts[0] = 'Calling mates ඞ...\n\n' + texts[0]

    for text in texts:
        await send_message(event, text)
