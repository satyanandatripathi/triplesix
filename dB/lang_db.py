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


import sqlite3

conn = sqlite3.connect("chat.db")
cur = conn.cursor()

try:
    cur.execute(
        """CREATE TABLE chat_ids
               (chat text, lang text)"""
    )
except sqlite3.OperationalError:
    pass


def add_chat(chat_id: int, lang="en"):
    x = get(chat_id)
    if not x:
        cur.execute(f"INSERT INTO chat_ids VALUES ({chat_id}, '{lang}')")
        conn.commit()
    else:
        print("have")


def set_lang(chat_id: int, lang: str):
    cur.execute(
        f"""UPDATE chat_ids
    SET chat = {chat_id}, lang = '{lang}'
    WHERE chat = {chat_id}
    """)
    conn.commit()


def del_chat(chat_id: int):
    cur.execute(f"DELETE FROM chat_ids WHERE chat = {chat_id}")
    conn.commit()


def get(chat_id: int):
    return list(cur.execute(f"SELECT * FROM chat_ids WHERE chat = {chat_id}"))
