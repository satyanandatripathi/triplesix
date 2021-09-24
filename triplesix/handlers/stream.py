from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from triplesix.functions import command, authorized_users_only
from triplesix.clients import player
from youtube_search import YoutubeSearch


def inline_keyboard(query: str, user_id: int):
    i = 0
    for j in range(3):
        i += 1
        yield InlineKeyboardButton(f"{i}", callback_data=f"stream {j}|{query}|{user_id}")


def inline_keyboard2(query: str, user_id: int):
    i = 3
    j = 2
    for _ in range(2):
        i += 1
        j += 1
        yield InlineKeyboardButton(f"{i}", callback_data=f"stream {j}|{query}|{user_id}")


@Client.on_message(command("stream"))
async def start_stream(_, message: Message):
    query = " ".join(message.command[1:])
    reply = message.reply_to_message
    if query:
        await player.start_stream(query, message)
    elif reply:
        if reply.video or reply.document:
            await message.reply("This feature is under development, contact @shohih_abdul2 for more information")
        else:
            await message.reply("Reply to video or document.\nNote: This feature is under development")
    else:
        await message.reply("Pass the query after /stream command!")


@Client.on_message(command("streamv2"))
async def stream_v2(_, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    rez = "\n"
    j = 0
    for i in range(5):
        j += 1
        res = YoutubeSearch(query, 5).to_dict()
        rez += f"{j}. [{res[i]['title'][:35]}...](https://youtube.com{res[i]['url_suffix']})\n"
        rez += f"Duration - {res[i]['duration']}\n"
        i += 1
    await message.reply(rez, reply_markup=InlineKeyboardMarkup(
        [
            list(inline_keyboard(query, user_id)),
            list(inline_keyboard2(query, user_id)),
            [
                InlineKeyboardButton("Close", f"close|{user_id}")
            ]
        ]
    ), disable_web_page_preview=True)
