# Ported from github.com/levina-lab
# with some change

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from triplesix.clients import bot, user


@Client.on_message(filters.command("start") & filters.private)
async def start_(_, message: Message):
    bot_username = (await bot.get_me()).username
    await message.reply_text(
        f"""<b>✨ **Welcome {message.from_user.mention()}** \n
		💭 **I'm a video streamer bot, i can streaming video from youtube trough the telegram group video chat !**
		❔ **To know how to use me click** /help</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add me to your Group ➕",
                        url=f"https://t.me/{bot_username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton("Dev", url="https://t.me/shohih_abdul2"),
                ],
            ]
        ),
    )


@Client.on_message(filters.command("help") & filters.group)
async def help_(_, message: Message):
    user_id = message.from_user.id
    client_username = (await user.get_me()).username
    await message.reply_text(
        f"""❓ HOW TO USE THIS BOT:
1.) first, add me to your group.
2.) then promote me as admin and give all permissions except anonymous admin.
3.) add @{client_username} to your group.
4.) turn on the voice chat first before start to stream video.
5.) type /stream (reply to video/give yt url) to start streaming.
6.) type /end to end the video streaming.
""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="🗑 Close", callback_data=f"close|{user_id}")]]
        ),
    )
