
from typing import Union, List

from pyrogram import filters

from config import COMMAND_PREFIXES


def is_edited(_, __, message):
    return message.edit_date is not None


edited = filters.create(is_edited, "edited")

other_filters = filters.group & ~edited & ~filters.via_bot & ~filters.forwarded
other_filters2 = filters.private & ~edited & ~filters.via_bot & ~filters.forwarded


def command(commands: Union[str, List[str]]):
    return filters.command(commands, COMMAND_PREFIXES)
    
