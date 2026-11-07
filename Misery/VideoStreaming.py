import asyncio
import re

from pyrogram import Client, filters
from pyrogram.types import Message

from pytgcalls import PyTgCalls
from pytgcalls.types import AudioQuality, MediaStream, VideoQuality
from yt_dlp import YoutubeDL

from config import API_ID, API_HASH, ASSISTANT_SESSION, BOT_USERNAME
from Misery import Misery
from helpers.decorators import authorized_users_only
from helpers.filters import command, edited


app = Client(
    "Misery",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=ASSISTANT_SESSION,
)

call_py = PyTgCalls(app)

VIDEO_CALL = set()


ydl_opts = {
    "format": "best[ext=mp4]/best",
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
}


def get_video_url(url):
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        if "entries" in info:
            info = next(iter(info["entries"]), None)

        if not info or not info.get("url"):
            raise Exception("Video bağlantısı alınamadı.")

        return info["url"]


@Misery.on_message(
    command(["vplay", f"vplay@{BOT_USERNAME}"])
    & filters.group
    & ~edited
)
async def vstream(_, m: Message):
    chat_id = m.chat.id

    if chat_id in VIDEO_CALL:
        await m.reply_text("Önce mevcut yayını /stop ile durdur.")
        return

    media = m.reply_to_message
    parts = (m.text or "").split(maxsplit=1)

    msg = await m.reply_text("🎬 Video hazırlanıyor...")

    try:
        if len(parts) > 1:
            query = parts[1].strip()

            if not query.startswith(("http://", "https://")):
                raise Exception("Lütfen geçerli bir video bağlantısı gönder.")

            stream = query

            if re.search(
                r"(youtube\.com|youtu\.be)",
                query,
                re.IGNORECASE,
            ):
                stream = await asyncio.to_thread(get_video_url, query)

        elif media and (media.video or media.document):
            if media.document and not (
                media.document.mime_type
                and media.document.mime_type.startswith("video/")
            ):
                raise Exception("Yanıt verdiğin dosya video değil.")

            stream = await media.download()

            if not stream:
                raise Exception("Video indirilemedi.")

        else:
            raise Exception(
                "Bir video bağlantısı gönder veya video dosyasına yanıt ver."
            )

        await call_py.play(
            chat_id,
            MediaStream(
                stream,
                AudioQuality.HIGH,
                VideoQuality.HD_720p,
            ),
        )

        VIDEO_CALL.add(chat_id)

        await msg.edit("✅ Video yayını başladı!")

    except Exception as e:
        await msg.edit(f"❌ Video yayın hatası:\n`{e}`")


@Misery.on_message(
    command(["stop", f"stop@{BOT_USERNAME}"])
    & filters.group
    & ~edited
)
@authorized_users_only
async def stop(_, m: Message):
    chat_id = m.chat.id

    if chat_id not in VIDEO_CALL:
        await m.reply_text("Aktif bir yayın bulunamadı.")
        return

    try:
        await call_py.leave_call(chat_id)
        VIDEO_CALL.discard(chat_id)

        await m.reply_text("⏹ Yayın durduruldu.")

    except Exception as e:
        await m.reply_text(f"❌ Yayın durdurulamadı:\n`{e}`")
