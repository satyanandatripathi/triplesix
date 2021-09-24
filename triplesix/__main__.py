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
from triplesix.clients import bot, player, user
from triplesix import bot_username, client_username

if not path.exists("downloads"):
    mkdir("downloads")

botname = bot_username
clientname = client_username


async def get_username():
    global botname
    x = await bot.get_me()
    botname += x.username


async def get_client_username():
    global clientname
    y = await user.get_me()
    clientname += y.username


player.call.start()
user.run(get_client_username())
bot.start()
bot.run(get_username())
print(f"Bot Started \nBot username: {bot_username}\nClient username: {client_username}")
print("=====Bot Running=====\n")

idle()
