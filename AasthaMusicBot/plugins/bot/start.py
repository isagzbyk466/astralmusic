#
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython import VideosSearch

import config
from config import BANNED_USERS
from config.config import OWNER_ID
from strings import get_command, get_string
from AasthaMusicBot import Telegram, YouTube, app
from AasthaMusicBot.misc import SUDOERS
from AasthaMusicBot.plugins.play.playlist import del_plist_msg
from AasthaMusicBot.plugins.sudo.sudoers import sudoers_list
from AasthaMusicBot.utils.database import (
    add_served_chat,
    add_served_user,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from AasthaMusicBot.utils.decorators.language import language
from AasthaMusicBot.utils.inline import help_pannel, private_panel, start_pannel


@app.on_message(
    filters.command(get_command("START_COMMAND")) & filters.private & ~BANNED_USERS
)
@language
async def start_comm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "yardım":
            keyboard = help_pannel(_)
            return await message.reply_text(_["help_1"], reply_markup=keyboard)
        if name[0:4] == "şarkı":
            return await message.reply_text(_["song_2"])
        if name[0:3] == "statü":
            m = await message.reply_text("🔎 kişisel istatistikler getiriliyor")
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if tot > 10:
                tracks = 10
            else:
                tracks = tot
            if not stats:
                return await m.edit(_["ustats_1"])
            msg = ""
            limit = 0
            results = {}
            for i in stats:
                top_list = stats[i]["spot"]
                results[str(i)] = top_list
                list_arranged = dict(
                    sorted(
                        results.items(),
                        key=lambda item: item[1],
                        reverse=True,
                    )
                )
            if not results:
                return await m.edit(_["ustats_1"])
            tota = 0
            for vidid, count in list_arranged.items():
                tota += count
                if limit > 9:
                    continue
                if limit == 0:
                    thumbnail = await YouTube.thumbnail(vidid, True)
                limit += 1
                details = stats.get(vidid)
                title = (details["title"][:35]).title()
                if vidid == "telegram":
                    msg += f"🔗[Telegram Files and Audios](https://t.me/telegram) ** played {count} times**\n\n"
                else:
                    msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) ** played {count} times**\n\n"
            await m.delete()
            msg = _["ustats_2"].format(tot, tota, tracks) + msg
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} bot başladığı kontrol ediliyor k <code>SUDOLIST</code>\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                return await Telegram.send_split_text(message, lyrics)
            else:
                return await message.reply_text("Failed to get lyrics.")
        if name[0:3] == "sil":
            await del_plist_msg(client=client, message=message, _=_)
        if name[0:3] == "bilgi":
            m = await message.reply_text("🔎Bilgi Alınıyor")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🔍__**Video Parça Bilgileri"**__

❇️**Başlık:** {title}

⏳**Süre:** {duration} Mins
👀**Görüntülenme:** `{views}`
⏰**Yayınlanma Zamanı:** {published}
🎥**Kanal Adı:** {channel}
📎**Kanal Linki:** [Visit From Here]({channellink})
🔗**Video Linki:** [Link]({link})

⚡️ __Searched Powered By {config.MUSIC_BOT_NAME}__"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🎥 İzle ", url=f"{link}"),
                        InlineKeyboardButton(text="🔄 Kapat", callback_data="Kapat"),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} has just started bot to check <code>VIDEO INFORMATION</code>\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}",
                )
    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        out = private_panel(_, app.username, OWNER)
        if config.START_IMG_URL:
            try:
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_2"].format(config.MUSIC_BOT_NAME),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            except:
                await message.reply_text(
                    _["start_2"].format(config.MUSIC_BOT_NAME),
                    reply_markup=InlineKeyboardMarkup(out),
                )
        else:
            await message.reply_text(
                _["start_2"].format(config.MUSIC_BOT_NAME),
                reply_markup=InlineKeyboardMarkup(out),
            )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} has just started Bot.\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}",
            )


@app.on_message(
    filters.command(get_command("başlat")) & filters.group & ~BANNED_USERS
)
@language
async def testbot(client, message: Message, _):
    out = start_pannel(_)
    return await message.reply_text(
        _["start_1"].format(message.chat.title, config.MUSIC_BOT_NAME),
        reply_markup=InlineKeyboardMarkup(out),
    )


welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**Private Music Bot**\n\nOnly for authorized chats from the owner. Ask my owner to allow your chat first."
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                if chat_type != "supergrup":
                    await message.reply_text(_["start_6"])
                    return await app.leave_chat(message.chat.id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    _["start_3"].format(
                        config.MUSIC_BOT_NAME,
                        userbot.username,
                        userbot.id,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_4"].format(config.MUSIC_BOT_NAME, member.mention)
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_5"].format(config.MUSIC_BOT_NAME, member.mention)
                )
            return
        except:
            return
