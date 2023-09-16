
import logging

from telethon.events import NewMessage, ChatAction

from bot.loader import bot
from bot.utils.funcs import send_message


def logger(func):
    async def wrapper(event):
        if isinstance(event, NewMessage.Event):
            logging.info(f'{event.chat_id=} {event.sender_id=} {event.raw_text=}')
        elif isinstance(event, ChatAction.Event):
            logging.info(f'{event.chat_id=} {event.action_message.action=}')
        else:
            logging.info(event)
        return await func(event)
    return wrapper


def is_group(func):
    async def wrapper(event):
        if event.is_private:
            return await send_message(event, '❗️Add me to the group to use this command', reply=True)
        return await func(event)
    return wrapper


def type_action(func):
    async def wrapper(event):
        async with bot.action(event.chat_id, 'typing'):
            return await func(event)
    return wrapper
