
from os import path, getenv
from dotenv import load_dotenv

if path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()

admins = {}

# Telegram bot ayarları
BOT_TOKEN = getenv("BOT_TOKEN")
API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")

# Yardımcı hesap oturumu
SESSION_NAME = "Misery"
ASSISTANT_SESSION = getenv("ASSISTANT_SESSION")

# Genel ayarlar
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "180"))

SUDO_USERS = list(
    map(int, getenv("SUDO_USERS", "").split())
)

ASSISTANT_NAME = getenv(
    "ASSISTANT_NAME",
    "MiseryVideoStreamer"
)

BOT_USERNAME = getenv(
    "BOT_USERNAME",
    "MiseryStreamBot"
).lstrip("@")

COMMAND_PREFIXES = getenv(
    "COMMAND_PREFIXES",
    "/ ! . ?"
).split()

# Gerekli değişkenleri kontrol et
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN ayarlanmamış.")

if not API_ID or not API_HASH:
    raise ValueError("API_ID veya API_HASH ayarlanmamış.")

API_ID = int(API_ID)

if not ASSISTANT_SESSION:
    raise ValueError("ASSISTANT_SESSION ayarlanmamış.")
