import asyncio

from yt_dlp import YoutubeDL
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream

from Misery import Misery
from Misery.VideoStreaming import call_py, VIDEO_CALL
from helpers.filters import command, edited
from config import BOT_USERNAME


def get_audio_url(query):
    options = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(
            query if query.startswith(("http://", "https://"))
            else f"ytsearch1:{query}",
            download=False,
        )

        if "entries" in info:
            info = next(iter(info["entries"]), None)

        if not info:
            raise Exception("Şarkı bulunamadı.")

        return info["url"]


@Misery.on_message(
    command(["play", f"play@{BOT_USERNAME}"])
    & filters.group
    & ~edited
)
async def song(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Kullanım: /play şarkı adı")
        return

    chat_id = message.chat.id

    if chat_id in VIDEO_CALL:
        await message.reply_text("Önce mevcut yayını /stop ile durdur.")
        return

    msg = await message.reply_text("🎵 Şarkı hazırlanıyor...")

    try:
        query = message.text.split(None, 1)[1]
        stream = await asyncio.to_thread(get_audio_url, query)

        await call_py.play(
            chat_id,
            MediaStream(
                stream,
                video_flags=MediaStream.Flags.IGNORE
            )
        )

        VIDEO_CALL.add(chat_id)
        await msg.edit("🎵 Müzik yayını başladı!")

    except Exception as e:
        await msg.edit(f"❌ Yayın hatası:\n`{e}`")ons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Close", callback_data="cls")]]
        )

        await k.edit("📤 **ᴜᴘʟᴏᴀᴅɪɴɢ ғɪʟᴇ...**")

        await message.reply_video(
            video_file,
            caption=caption,
            duration=duration,
            thumb=thumb_name,
            reply_markup=buttons,
            supports_streaming=True,
        )

        await k.delete()

    except Exception as e:
        await k.edit(
            f"❌ **sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ! "
            f"ʀᴇᴘᴏʀᴛ ᴛᴏ @MiserySupport**\n`{e}`"
        )

    finally:
        try:
            if video_file and os.path.exists(video_file):
                os.remove(video_file)

            if os.path.exists(thumb_name):
                os.remove(thumb_name)

        except Exception as e:
            print(e)


# Edited By TurdusMaximus

