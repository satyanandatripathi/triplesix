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

from triplesix.functions import command, authorized_users_only
from triplesix.clients import player

"""
This method is only can used by admin or sudo users
"""


@Client.on_message(command("pause"))
@authorized_users_only
async def pause_current_playing(_, message: Message):
    await player.change_stream_status("pause", message)


@Client.on_message(command("resume"))
@authorized_users_only
async def resume_current_playing(_, message: Message):
    await player.change_stream_status("resume", message)


@Client.on_message(command("vol"))
@authorized_users_only
async def change_volume_bot(_, message: Message):
    await player.change_vol(message)


@Client.on_message(command("end"))
@authorized_users_only
async def end_stream(_, message: Message):
    await player.end_stream(message)


@Client.on_message(command("skip"))
@authorized_users_only
async def skip_current_playing(_, message: Message):
    await player.change_stream(message)
