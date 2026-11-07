import asyncio
from pyrogram import idle

from Misery import Misery
from Misery.VideoStreaming import app, call_py


async def main():
    try:
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

        await idle()

    finally:
        if app.is_connected:
            await app.stop()

        if Misery.is_connected:
            await Misery.stop()


if __name__ == "__main__":
    asyncio.run(main())
