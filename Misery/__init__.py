from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

Misery = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Misery")
)
