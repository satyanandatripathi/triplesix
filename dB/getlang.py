import json
from os import path, listdir

from dB.lang_db import get
lang_folder = path.join(path.dirname(path.realpath(__file__)), "lang")

code = ""
langs = {}
kode = []
for file in listdir(lang_folder):
    if file.endswith(".json"):
        code = file[:-5]
        kode.append(file[:-5])
        langs[code] = json.load(
            open(path.join(lang_folder, file), encoding="UTF-8"),
        )


def get_message(chat_id: int, key: str):
    try:
        return langs[get(chat_id)[0][1]][key]
    except KeyError:
        return f"Warning: \nCan't get the lang with key: {key}"
