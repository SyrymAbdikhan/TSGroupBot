
import logging
import re

from telethon import events

from bot.loader import bot
from bot.utils.funcs import *
from bot.utils.decorators import logger


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
                              '/fdl - formats deadlines of original message\n'
                              '/help - more information about bot\n\n'
                              'Developer contacts: @Honey_Niisan')


@bot.on(events.NewMessage(pattern=r'/fdl'))
@logger
async def cmd_fdl(event):
    if not event.is_reply:
        return await send_message(event, 'To use this command, please reply to message with deadlines', reply=True)

    message = await event.get_reply_message()
    text = message.raw_text
    
    new_text = re.sub("\n\d+\. ", "\n\n===========\n", text)
    new_text = re.sub(" \| ", "\n", new_text)

    await send_message(event, new_text, reply=True)


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
