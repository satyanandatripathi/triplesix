# Ported from github.com/levina-lab
# with some change

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from triplesix.clients import bot, user
from triplesix.configs import config


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
						"➕ Add me to your Group ➕", url=f"https://t.me/{bot_username}?startgroup=true")
				],
				[
					InlineKeyboardButton(
						"Dev", url="https://t.me/shohih_abdul2"),
				],
				[
					InlineKeyboardButton(
						"💭 Group", url=f"{config.GROUP_URL}"
					),
					InlineKeyboardButton(
						"Channel", url=f"{config.CHANNEL_URL}"
					)
				]
			]
		)
	)


@Client.on_message(filters.command("help"))
async def help_(_, message: Message):
	user_id = message.from_user.id
	client_username = (await user.get_me()).username
	chat_type = message.chat.type
	if chat_type == "supergroup":
		await message.reply(
			f"""How To Use This Bot:
		1. make me as administrator
		2. add @{client_username} to this group
		3. type /stream or /streamv2 and give the title to start streaming
		4. type /end if you want to end the streaming
		""",
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							text="🗑 Close", callback_data=f"close|{user_id}"
						)
					]
				])
		)
		return
	if chat_type == "private":
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
				[
					[
						InlineKeyboardButton(
							text="🗑 Close", callback_data=f"close|{user_id}"
						)
					]
				]
			),
		)
