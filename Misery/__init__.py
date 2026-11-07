from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

Misery = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={
        "root": "Misery",
        "include": [
            "PmText",
            "VideoStreaming",
            "song",
            "ytsearch",
            "MiseryInlineSearch",
        ],
    },
)
