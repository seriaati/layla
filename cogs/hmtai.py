import typing

import discord
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands

from dev.model import BotModel, ErrorEmbed
from utility.paginator import GeneralPaginator
from utility.utils import get_json


class HmtaiCog(commands.GroupCog, name="hmtai"):
    def __init__(self, bot):
        self.bot: BotModel = bot

    async def cog_load(self) -> None:
        self.sfw_endpoints: typing.Optional[typing.List[str]] = get_json(
            "hmtai_endpoints.json"
        ).get("sfw")
        self.nsfw_endpoints: typing.Optional[typing.List[str]] = (
            get_json("hmtai_endpoints.json")
        ).get("nsfw")

    async def get_image(self, endpoint: str) -> str:
        async with self.bot.session.get(
            f"https://hmtai.hatsunia.cfd/v2/{endpoint}"
        ) as resp:
            if resp.status != 200:
                return ""
            data: typing.Dict[str, str] = await resp.json()
            return data["url"]

    async def run_command(self, i: discord.Interaction, endpoint: str, num: int):
        await i.response.defer(ephemeral=True)
        embeds: typing.List[discord.Embed] = []

        for _ in range(num):
            image = await self.get_image(endpoint)
            if not image:
                return await i.response.send_message(
                    embed=ErrorEmbed(
                        title="查詢失敗",
                        description="請檢查您輸入的標籤是否正確",
                    ),
                    ephemeral=True,
                )

        await GeneralPaginator(i, embeds).start(ephemeral=True, followup=True)

    @app_commands.command(name="sfw", description=_T("Search sfw images by tags"))
    @app_commands.rename(endpoint=_T("tags"), num=_T("num"))
    @app_commands.describe(
        endpoint=_T("The tags to search for"), num=_T("he number of images to return")
    )
    async def sfw(
        self,
        i: discord.Interaction,
        endpoint: str,
        num: app_commands.Range[int, 1, 20] = 1,
    ):
        await self.run_command(i, endpoint, num)

    @app_commands.command(name="nsfw", description=_T("Search nsfw images by tags"))
    @app_commands.rename(endpoint=_T("tags"), num=_T("num"))
    @app_commands.describe(
        endpoint=_T("The tags to search for"), num=_T("The number of images to return")
    )
    async def nsfw(
        self,
        i: discord.Interaction,
        endpoint: str,
        num: app_commands.Range[int, 1, 20] = 1,
    ):
        await self.run_command(i, endpoint, num)

    async def endpoint_autocomplete(self, tag_type: str, current: str):
        endpoints = self.sfw_endpoints if tag_type == "sfw" else self.nsfw_endpoints
        if not endpoints:
            return []
        return [
            app_commands.Choice(name=_T(tag), value=tag)
            for tag in endpoints
            if current.lower() in tag.lower()
        ][:25]

    @sfw.autocomplete("endpoint")
    async def sfw_autocomplete(self, _: discord.Interaction, current: str):
        return await self.endpoint_autocomplete("sfw", current)

    @nsfw.autocomplete("endpoint")
    async def nsfw_autocomplete(self, _: discord.Interaction, current: str):
        return await self.endpoint_autocomplete("nsfw", current)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HmtaiCog(bot))
