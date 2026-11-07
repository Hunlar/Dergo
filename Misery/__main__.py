
import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from Misery.VideoStreaming import app


Misery = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Misery"),
)


async def main():
    await Misery.start()
    print("[Your Misery Is Ready To Stream]")

    await app.start()
    print("Started Successfully")

    await idle()

    await app.stop()
    await Misery.stop()


if __name__ == "__main__":
    asyncio.run(main())
    
