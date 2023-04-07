import typing

import discord
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands

from dev.model import BotModel, DefaultEmbed, translator
from ui.TagSelect import TagSelectView
from utility.utils import get_json


class WaifuimCog(commands.GroupCog, name="waifuim"):
    def __init__(self, bot):
        self.bot: BotModel = bot

    async def cog_load(self) -> None:
        self.tags: typing.Dict[str, typing.List[str]] = get_json("waifuim_tags.json")

    @app_commands.command(name="search", description=_T("Search images by tags"))
    async def sfw(
        self,
        i: discord.Interaction,
    ):
        view = TagSelectView(self.tags, i.locale)
        embed = DefaultEmbed(translator.trans("Search images by tags", i.locale))
        await i.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WaifuimCog(bot))
