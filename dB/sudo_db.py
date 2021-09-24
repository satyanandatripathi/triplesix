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


import sqlite3 as sql
from typing import Iterable

conn = sql.connect("chat.db")
cur = conn.cursor()

try:
    cur.execute("""CREATE TABLE sudo_table 
                (chat_id integer, user_id integer)""")
except sql.OperationalError:
    pass


def add_sudo(chat_id: int, user_id: int):
    """Function for add sudo in the chat"""
    if user_id in get_sudos(chat_id):
        return
    cur.execute(f"INSERT INTO sudo_table VALUES ({chat_id}, {user_id})")
    conn.commit()


def del_sudo(chat_id: int, user_id: int):
    """Function for delete sudo on the chat"""
    cur.execute(f"DELETE FROM sudo_table WHERE user_id = {user_id} AND chat_id = {chat_id}")
    conn.commit()


def get_sudos(chat_id: int) -> Iterable[int]:
    """Function for get all sudos in the chat"""
    return [row[1] for row in cur.execute(f"SELECT * FROM sudo_table WHERE chat_id = {chat_id}")]
