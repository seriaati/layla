import logging
import typing

import aiofiles
from discord.ext import commands, tasks

from data.endpoints import HMTAI_ENDPOINTS, WAIFUIM_TAGS
from data.file_names import HMTAI_JSON, WAIFUIM_JSON
from dev.model import BotModel


class ScheduleCog(commands.Cog):
    def __init__(self, bot):
        self.bot: BotModel = bot

    async def cog_load(self):
        self.run_tasks.start()

    @tasks.loop(seconds=1)
    async def run_tasks(self):
        await self.update_waifu_im_tags()
        await self.update_hmtai_endpoints()

    @run_tasks.before_loop
    async def before_run_tasks(self):
        await self.bot.wait_until_ready()

    async def update_waifu_im_tags(self):
        """Update waifu.im tags."""
        logging.info("Updating waifu.im tags...")

        async with self.bot.session.get(WAIFUIM_TAGS) as resp:
            if resp.status != 200:
                return
            data: typing.Dict[str, typing.List[str]] = await resp.json()
            async with aiofiles.open(WAIFUIM_JSON, "w") as f:
                await f.write(data)

        logging.info("Updated waifu.im tags.")

    async def update_hmtai_endpoints(self):
        """Update hmtai endpoints."""
        logging.info("Updating hmtai endpoints...")

        async with self.bot.session.get(HMTAI_ENDPOINTS) as resp:
            if resp.status != 200:
                return
            data: typing.Dict[str, typing.Any] = await resp.json()
            async with aiofiles.open(HMTAI_JSON, "w") as f:
                await f.write(data)

        logging.info("Updated hmtai endpoints.")
