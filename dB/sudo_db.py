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
