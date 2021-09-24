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
