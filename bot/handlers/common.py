
from telethon import events
from telethon.tl.types import MessageActionChatAddUser, MessageActionChatDeleteUser

from bot.loader import bot
from bot.utils.funcs import send_message, get_db
from bot.utils.decorators import logger, type_action
from bot.db.models import ChatSettings


@bot.on(events.NewMessage(pattern=r'/start'))
@logger
@type_action
async def cmd_start(event: events.NewMessage.Event) -> None:
    await send_message(event, 'Hi! I\'m assistant bot for groups. '
                              'Type /help for more information')


@bot.on(events.NewMessage(pattern=r'/help'))
@logger
@type_action
async def cmd_help(event: events.NewMessage.Event) -> None:
    text = 'Here is the bot commands:\n\n' \
           '/call - mention all members of the group\n' \
           '/deadlines - shows all deadlines\n' \
           '/newq - creates new queue\n' \
           '/settoken - sets moodle token to get deadlines\n' \
           '/help - more information about bot\n\n' \
           'To get token, go to moodle > profile > ⚙️ Security keys > Moodle mobile web service\n\n' \
           'Developer contacts: @Honey_Niisan'

    await send_message(event, text, reply=True)


@bot.on(events.ChatAction())
@logger
async def chat_action(event: events.ChatAction.Event) -> None:
    db_session = await get_db(bot.db)
    
    chat = await ChatSettings.find(db_session, event.chat_id)
    if chat is None:
        chat = ChatSettings(chat_id=event.chat_id)
    
    if isinstance(event.action_message.action, MessageActionChatDeleteUser):
        if bot.config.id == event.action_message.action.user_id:
            if chat.active:
                chat.active = False
            await chat.save(db_session)
            return await db_session.close()
    
    if isinstance(event.action_message.action, MessageActionChatAddUser):
        if bot.config.id in event.action_message.action.users:
            if not chat.active:
                chat.active = True
            await chat.save(db_session)
            
            await send_message(event, '🥳 Hello mates! I\'m assistant bot for your group. '
                                      'Type /help for more information')
            return await db_session.close()
    
    if event.user_joined or event.user_added:
        await send_message(event, '🥳 Welcome to the group mate!')
    elif event.user_left or event.user_kicked:
        await send_message(event, '💔 Press F to pay respect...')
    
    await db_session.close()
