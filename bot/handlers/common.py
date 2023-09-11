
from telethon import events

from bot.loader import bot
from bot.utils.funcs import send_message
from bot.utils.decorators import logger


@bot.on(events.NewMessage(pattern=r'/start'))
@logger
async def cmd_start(event):
    await send_message(event, 'Hello! I\'m assistant bot for your group.'
                              'Type /help for more information')


@bot.on(events.NewMessage(pattern=r'/help'))
@logger
async def cmd_help(event):
    text = 'Here is the bot commands:\n\n' \
           '/call - mention all members of the group\n' \
           '/deadlines - shows all deadlines\n' \
           '/settoken - sets moodle token to get deadlines\n' \
           '/help - more information about bot\n\n' \
           'To get token, go to moodle > profile > ⚙️ Security keys > Moodle mobile web service\n\n' \
           'Developer contacts: @Honey_Niisan'

    await send_message(event, text, reply=True)


@bot.on(events.ChatAction())
@logger
async def chat_action(event):
    if event.user_joined or event.user_added:
        await send_message(event, '🥳 Welcome to the group mate!')
    elif event.user_left or event.user_kicked:
        await send_message(event, '💔 Press F to pay respect...')
