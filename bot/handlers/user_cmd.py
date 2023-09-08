
from telethon import events

from bot.loader import bot
from bot.utils.funcs import *
from bot.utils.decorators import logger


@bot.on(events.NewMessage(pattern=r'^(/|@)all'))
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
