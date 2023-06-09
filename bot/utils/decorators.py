
import logging

from telethon.events import NewMessage, ChatAction


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

