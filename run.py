import os
import sys

import aiohttp
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class Layla(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            application_id=os.getenv("APP_ID"),
            intents=Intents.default(),
        )
    
    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        await self.load_extension(f"cogs.waifu")
        
        self.session = aiohttp.ClientSession()


if sys.platform == "linux1" or sys.platform == "linux2":
    import uvloop  # type: ignore

    uvloop.install()

bot = Layla()
bot.run(os.getenv("TOKEN"))
