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


from pyrogram import Client
from pyrogram.types import Message

from dB.getlang import get_message, kode
from dB.lang_db import set_lang
from triplesix.functions import command, authorized_users_only


@Client.on_message(command("lang"))
@authorized_users_only
async def change_lang(_, message: Message):
    lang = "".join(message.command[1])
    if len(lang) > 2:
        await message.reply("Use the international format (2 characters)")
        return
    if len(lang) == 0:
        x = "\n- ".join(kode)
        await message.reply(
            f"here some lang that supported with this bot, to change lang, use /lang (langcode) \n\n- {x}"
        )
        return
    chat_id = message.chat.id
    set_lang(chat_id, lang)
    await message.reply(get_message(chat_id, "changed").format(lang))
