
import re

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from youtube_dl import YoutubeDL

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
    "geo-bypass": True,
    "nocheckcertificate": True,
}

ydl = YoutubeDL(ydl_opts)


@Misery.on_message(
    command(["vplay", f"vplay@{BOT_USERNAME}"])
    & filters.group
    & ~edited
)
async def vstream(_, m: Message):
    chat_id = m.chat.id

    if chat_id in VIDEO_CALL:
        await m.reply_text("Önce mevcut yayını /stop ile durdurmalısın.")
        return

    media = m.reply_to_message
    parts = (m.text or "").split(maxsplit=1)

    if len(parts) > 1:
        query = parts[1].strip()
        msg = await m.reply_text("🔄 Yayın hazırlanıyor...")

        ytstream = query

        if re.match(
            r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+",
            query,
        ):
            try:
                info = ydl.extract_info(query, download=False)
                formats = info.get("formats", [])

                ytstream = next(
                    (
                        f["url"]
                        for f in reversed(formats)
                        if f.get("url") and f.get("vcodec") != "none"
                    ),
                    None,
                )

                if not ytstream:
                    raise Exception("Oynatılabilir video bulunamadı.")

            except Exception as e:
                await msg.edit(f"❌ YouTube hatası: `{e}`")
                return

        try:
            await call_py.play(chat_id, ytstream)
            VIDEO_CALL.add(chat_id)
            await msg.edit("✅ Yayın başladı!")

        except Exception as e:
            await msg.edit(f"❌ Yayın başlatılamadı:\n`{e}`")

        return

    if media and (media.video or media.document):
        if media.document and not (
            media.document.mime_type
            and media.document.mime_type.startswith("video/")
        ):
            await m.reply_text("Lütfen video dosyasına yanıt ver.")
            return

        msg = await m.reply_text("📥 Video hazırlanıyor...")

        try:
            video = await media.download()

            if not video:
                raise Exception("Video indirilemedi.")

            await call_py.play(chat_id, video)
            VIDEO_CALL.add(chat_id)

            await msg.edit("✅ Video yayını başladı!")

        except Exception as e:
            await msg.edit(f"❌ Yayın başlatılamadı:\n`{e}`")

        return

    await m.reply_text(
        "Bir YouTube bağlantısı gönder veya bir video mesajına yanıt ver."
    )


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
