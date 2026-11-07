import asyncio
from pyrogram import idle
from Misery import Misery
from Misery.VideoStreaming import app


async def main():
    await Misery.start()
    print("Bot başlatıldı.")

    await app.start()
    print("Yardımcı hesap başlatıldı.")

    await idle()

    await app.stop()
    await Misery.stop()


if __name__ == "__main__":
    asyncio.run(main())
