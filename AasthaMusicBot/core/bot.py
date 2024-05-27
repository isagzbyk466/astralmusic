import sys

from pyrogram import Client

import config

from ..logging import LOGGER


class AlexaBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Bot Başlıyor..")
        super().__init__(
            "GorilMüzik",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        try:
            await self.send_message(
                config.LOG_GROUP_ID, "GorilMüzik Başladı"
            )
        except:
            LOGGER(__name__).error(
                "Bot, günlük grubuna erişemedi. Botunuzu günlük kanalına eklediğinizden ve yönetici olarak tanımladığınızdan emin olun!"
            )
            sys.exit()
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != "yönetici":
            LOGGER(__name__).error("Lütfen Bot'u Günlük Grubunda yönetici olarak tanıtın")
            sys.exit()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"Müzik Botu Başladı as {self.name}")
