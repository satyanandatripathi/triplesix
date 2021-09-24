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


from os import path, mkdir
from pyrogram import idle
from triplesix.clients import bot, player
from triplesix import bot_username

if not path.exists("downloads"):
    mkdir("downloads")


async def get_username():
    global bot_username
    x = await bot.get_me()
    bot_username += x.username


player.call.start()
bot.start()
bot.run(get_username())
print(f"DON'T DELETE THIS, THIS IS FOR DEBUG \nBot username: {bot_username}")
print("=====Bot Running=====\n")

idle()
