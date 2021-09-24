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
