import asyncio
import random

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, CallbackQuery
from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import NoActiveGroupCall, GroupCallNotFound
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import MediumQualityAudio, MediumQualityVideo
from pytgcalls.types import Update

from dB import get_message
from triplesix.configs import config
from triplesix.functions import get_youtube_stream

user = Client(config.SESSION, config.API_ID, config.API_HASH)

bot = Client(
    ":memory:",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="triplesix.handlers"),
)


class Player:
    def __init__(self, pytgcalls: PyTgCalls):
        self.call = pytgcalls
        self.client = {}
        self.playlist: dict[int, list[dict[str, str]]] = {}

    async def _stream(self, query: str, message: Message, url: str, y):
        chat_id = message.chat.id
        playlist = self.playlist
        playlist[chat_id] = [{"query": query}]
        call = self.call
        await y.edit(get_message(chat_id, "stream").format(query))
        await call.join_group_call(
            chat_id,
            AudioVideoPiped(url, MediumQualityAudio(), MediumQualityVideo()),
            stream_type=StreamType().pulse_stream,
        )
        self.client[chat_id] = call

    async def _start_stream(self, query, message: Message):
        chat_id = message.chat.id
        playlist = self.playlist
        if len(playlist) >= 1:
            try:
                playlist[chat_id].extend([{"query": query}])
                y = await message.reply("Queued")
                await asyncio.sleep(10)
                await y.delete()
                return
            except KeyError:
                await message.reply("restart the bot")
                del playlist[chat_id]
                return
        y = await message.reply(get_message(chat_id, "process"))
        url = await get_youtube_stream(query)
        try:
            await self._stream(query, message, url, y)
        except FloodWait as fw:
            await message.reply(f"Getting floodwait {fw.x} second, bot sleeping")
            await asyncio.sleep(fw.x)
            await self._stream(query, message, url, y)
        except NoActiveGroupCall:
            try:
                await user.send(
                    CreateGroupCall(
                        peer=await user.resolve_peer(chat_id),
                        random_id=random.randint(10000, 999999999),
                    )
                )
                await self._stream(query, message, url, y)
            except Exception as ex:
                await y.edit(
                    f"{type(ex).__name__}: {ex.with_traceback(ex.__traceback__)}"
                )
                del playlist[chat_id]
        except Exception as ex:
            await y.edit(f"{type(ex).__name__}: {ex.with_traceback(ex.__traceback__)}")
            del playlist[chat_id]

    async def start_stream(self, query: str, message: Message):
        await self._start_stream(query, message)

    async def start_stream_via_callback(self, query: str, callback: CallbackQuery):
        message = callback.message
        await self._start_stream(query, message)

    async def change_stream(self, message: Message):
        playlist = self.playlist
        client = self.client
        chat_id = message.chat.id
        if len(playlist[chat_id]) > 1:
            playlist[chat_id].pop(0)
            query = playlist[chat_id][0]['query']
            url = await get_youtube_stream(query)
            await asyncio.sleep(3)
            await client[chat_id].change_stream(
                chat_id,
                AudioVideoPiped(url, MediumQualityAudio(), MediumQualityVideo()),
                stream_type=StreamType().pulse_stream
            )
            await asyncio.sleep(3)
            await message.reply(f"Skipped track, and playing {query}")
            return
        await message.reply("No playlist")

    async def end_stream(self, message: Message):
        chat_id = message.chat.id
        playlist = self.playlist
        client = self.client
        try:
            try:
                if client[chat_id].get_call(chat_id):
                    await client[chat_id].leave_group_call(chat_id)
                    del playlist[chat_id]
                    await message.reply("ended")
            except KeyError:
                await message.reply("you never streaming anything")
        except GroupCallNotFound:
            await message.reply("not streaming")

    async def change_stream_status(self, status: str, message: Message):
        if status == "pause":
            client = self.client
            chat_id = message.chat.id
            if client[chat_id].get_call(chat_id):
                await client[chat_id].pause_stream(chat_id)
                await message.reply("Bot paused")
                return
            return
        elif status == "resume":
            client = self.client
            chat_id = message.chat.id
            if client[chat_id].get_call(chat_id):
                await client[chat_id].resume_stream(chat_id)
                await message.reply("Bot resume")
                await asyncio.sleep(5)
                await message.delete()
                return
            return

    async def change_vol(self, message: Message):
        vol = int("".join(message.command[1]))
        client = self.client
        chat_id = message.chat.id
        if client[chat_id].get_call(chat_id):
            await client[chat_id].change_volume_call(chat_id, vol)
            await message.reply(f"Volume changed to {vol}%")
    

player = Player(PyTgCalls(user))
@player.call.on_stream_end()
async def stream_ended(pytgcalls: PyTgCalls, update: Update):
    playlist = player.playlist
    chat_id = update.chat_id
    client = player.client
    if len(playlist[chat_id]) > 1:
        playlist[chat_id].pop(0)
        query = playlist[chat_id][0]['query']
        url = await get_youtube_stream(query)
        await asyncio.sleep(3)
        await client[chat_id].change_stream(
            chat_id,
            AudioVideoPiped(url, MediumQualityAudio(), MediumQualityVideo()),
            stream_type=StreamType().pulse_stream
        )
        await asyncio.sleep(3)
        return
    await client.leave_group_call(chat_id)
    await asyncio.sleep(5)
