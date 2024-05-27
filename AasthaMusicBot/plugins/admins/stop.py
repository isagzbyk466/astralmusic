from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from AasthaMusicBot import app
from AasthaMusicBot.core.call import Alexa
from AasthaMusicBot.utils.decorators import AdminRightsCheck

# Commands
STOP_COMMAND = get_command("dur")


@app.on_message(filters.command(STOP_COMMAND) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    await Alexa.stop_stream(chat_id)
    await message.reply_text(_["admin_9"].format(message.from_user.mention))
