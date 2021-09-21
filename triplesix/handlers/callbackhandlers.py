from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from youtube_search import YoutubeSearch

from triplesix.clients import player


@Client.on_callback_query(filters.regex(pattern=r"close"))
async def close_inline(_, cb: CallbackQuery):
    await cb.message.delete()


@Client.on_callback_query(filters.regex(pattern=r"stream"))
async def play_callback(_, cb: CallbackQuery):
    callback = cb.data.split("|")
    x = int(callback[0].split(" ")[1])
    query = callback[1]
    user_id = int(callback[2])
    if cb.from_user.id != user_id:
        await cb.answer("this is not for u.", show_alert=True)
        return
    res = YoutubeSearch(query, 5).to_dict()
    title = res[x]["title"]
    await player.start_stream_via_callback(title, cb)
