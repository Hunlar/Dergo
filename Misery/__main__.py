
import asyncio
from pyrogram import idle

from Misery import Misery
from Misery.VideoStreaming import app, call_py


async def main():
    await Misery.start()
    print("Bot başlatıldı.")

    print("Handler grupları:", {
        group: len(handlers)
        for group, handlers in Misery.dispatcher.groups.items()
    })

    await app.start()
    print("Yardımcı hesap başlatıldı.")

    await call_py.start()
    print("PyTgCalls yayın motoru başlatıldı.")

    try:
        await idle()
    finally:
        await app.stop()
        await Misery.stop()


if __name__ == "__main__":
    asyncio.run(main())
