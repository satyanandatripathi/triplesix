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


from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from youtube_search import YoutubeSearch

from triplesix.clients import player


@Client.on_callback_query(filters.regex(pattern=r"close"))
async def close_inline(_, cb: CallbackQuery):
    callback = cb.data.split("|")
    user_id = int(callback[1])
    if cb.from_user.id != user_id:
        await cb.answer("this is not for you.", show_alert=True)
        return
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
