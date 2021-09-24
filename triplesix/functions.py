from typing import Callable

import asyncio
import requests
from pafy import new
from pyrogram import filters, Client
from pyrogram.types import Message
from youtube_search import YoutubeSearch

from triplesix import bot_username
from dB import get_sudos


def command(cmd: str):
    """
    Function for pyrogram command
    :param str cmd: the command
    """
    return filters.command([cmd, f"{cmd}@{bot_username}"])


async def get_youtube_stream(query: str):
    proc = await asyncio.create_subprocess_exec(
        "youtube-dl",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"https://youtube.com{YoutubeSearch(query, 1).to_dict()[0]['url_suffix']}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return stdout.decode().split("\n")[0]


def authorized_users_only(func: Callable) -> Callable:
    """Only authorized users (admin or sudo or owner) can use the command"""

    async def wrapper(client: Client, message: Message):
        if message.from_user.id in get_sudos(message.chat.id):
            return await func(client, message)

        person = await message.chat.get_member(message.from_user.id)
        if person.status == "creator" or person.status == "administrator":
            return await func(client, message)
    return wrapper


def video_downloader(query: str):
    url = f"https://youtube.com{YoutubeSearch(query, 1).to_dict()[0]['url_suffix']}"
    pufy = new(url)
    title = pufy.title[:30]
    thumbs = pufy.bigthumbhd
    thumb = requests.get(thumbs, allow_redirects=True)
    open(f"thumb{title}.jpg", "wb").write(thumb.content)
    dur = pufy.duration
    vid = pufy.getbestvideo()
    filename = vid.download(quiet=True)
    return dur, filename, title
