import asyncio

from pyrogram import filters
from pyrogram.types import ChatMemberUpdated, Message

from dB import add_chat, del_chat
from triplesix.clients import bot, user


@bot.on_chat_member_updated(filters=filters.group)
async def chat_member_updated(_, msg: ChatMemberUpdated):
    try:
        bot_id = (await bot.get_me()).id
        chat_id = msg.chat.id
        members = msg.new_chat_member.user
        lang = msg.new_chat_member.invited_by.language_code
        if members.id == bot_id:
            add_chat(chat_id, lang if lang else "en")
    except AttributeError:
        pass


@bot.on_message(filters=filters.left_chat_member)
async def on_bot_kicked(_, message: Message):
    try:
        bot_id = (await bot.get_me()).id
        chat_id = message.chat.id
        members = message.left_chat_member
        if members.id == bot_id:
            del_chat(chat_id)
            await user.send_message(chat_id, "bot left from chat, assistant left this chat too")
            await asyncio.sleep(3)
            await user.leave_chat(chat_id)
    except Exception as e:
        await message.reply(f"{e}")
