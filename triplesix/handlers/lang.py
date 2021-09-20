from pyrogram import Client
from pyrogram.types import Message

from dB.getlang import get_message
from dB.lang_db import set_lang
from triplesix.functions import command, authorized_users_only


@Client.on_message(command("lang"))
@authorized_users_only
async def change_lang(_, message: Message):
    lang = "".join(message.command[1])
    if len(lang) > 2:
        await message.reply("Use the international format (2 characters)")
        return
    chat_id = message.chat.id
    set_lang(chat_id, lang)
    await message.reply(get_message(chat_id, "changed").format(lang))
