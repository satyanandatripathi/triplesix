#     Video Stream Bot, by Abdul
#     Copyright (C) 2021  Shohih Abdul
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
