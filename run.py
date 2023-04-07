import asyncio
import glob
import logging
import os
import pathlib
import platform
import sys

import aiohttp
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from dev.model import BotModel, translator

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(), logging.FileHandler("log.log")],
)


class Layla(BotModel):
    def __init__(self, session: aiohttp.ClientSession):
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=Intents.default(),
        )
        self.session = session

    async def on_ready(self) -> None:
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def setup_hook(self) -> None:
        logging.info("Loading jishaku...")
        await self.load_extension("jishaku")

        logging.info("Loading cogs...")
        for file in glob.glob("cogs/*.py"):
            await self.load_extension(f"cogs.{pathlib.Path(file).stem}")


if platform.system() == "Linux":
    import uvloop  # type: ignore

    uvloop.install()


async def main() -> None:
    session = aiohttp.ClientSession()
    bot = Layla(session)
    await bot.tree.set_translator(translator)
    token = os.getenv("TOKEN")
    if token is None:
        logging.error("No token provided")
        sys.exit(1)

    async with (session, bot):
        try:
            await bot.start(token)
        except KeyboardInterrupt:
            return
        except Exception as e:
            logging.error("Failed to start bot", exc_info=e)
            return


asyncio.run(main())
