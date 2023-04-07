import logging
import typing

import aiohttp
import discord
from discord.ext import commands
from waifuim import WaifuAioClient

from utility.utils import get_yaml


class BotModel(commands.Bot):
    session: aiohttp.ClientSession
    user: discord.ClientUser
    wf: WaifuAioClient


class Inter(discord.Interaction):
    client: BotModel


class LaylaTranslator(discord.app_commands.Translator):
    def __init__(self) -> None:
        self.zh_tw = get_yaml("localization/zh-TW.yaml")
        self.zh_cn = get_yaml("localization/zh-CN.yaml")

    async def translate(
        self,
        string: discord.app_commands.locale_str,
        locale: discord.Locale,
        _: discord.app_commands.TranslationContextTypes,
    ) -> typing.Optional[str]:
        if locale == discord.Locale.taiwan_chinese:
            return self.zh_tw.get(string.message)
        elif locale == discord.Locale.chinese:
            return self.zh_cn.get(string.message)
        else:
            return None

    def trans(self, string: str, locale: discord.Locale) -> str:
        if locale == discord.Locale.taiwan_chinese:
            return self.zh_tw.get(string) or string
        elif locale == discord.Locale.chinese:
            return self.zh_cn.get(string) or string
        else:
            return string


translator = LaylaTranslator()


class ShenheEmbed(discord.Embed):
    def __init__(
        self,
        title: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        color: typing.Optional[int] = 0xA68BD3,
    ):
        super().__init__(title=title, description=description, color=color)


class DefaultEmbed(ShenheEmbed):
    def __init__(
        self,
        title: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
    ):
        super().__init__(title=title, description=description, color=0xA68BD3)


class ErrorEmbed(ShenheEmbed):
    def __init__(
        self,
        title: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
    ):
        super().__init__(title=title, description=description, color=0xFC5165)


class BaseView(discord.ui.View):
    def __init__(
        self,
        timeout: typing.Optional[float] = 600.0,
    ):
        super().__init__(timeout=timeout)
        self.message: typing.Optional[discord.Message] = None
        self.author: typing.Optional[typing.Union[discord.User, discord.Member]] = None

    def disable_items(self):
        """Disable all buttons and selects in the view."""
        for child in self.children:
            if isinstance(child, (discord.ui.Button, discord.ui.Select)):
                child.disabled = True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.author is None:
            return True
        elif interaction.user.id == self.author.id:
            return True
        else:
            embed = ErrorEmbed("錯誤", "你不是指令發送者")
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except discord.InteractionResponded:
                await interaction.followup.send(embed=embed)
            except Exception:
                pass
            return False

    async def on_timeout(self) -> None:
        if self.message is not None:
            for child in self.children:
                if isinstance(child, (discord.ui.Button, discord.ui.Select)):
                    child.disabled = True
            try:
                await self.message.edit(view=self)
            except Exception:
                pass

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: discord.ui.Item[typing.Any],
        /,
    ) -> None:
        logging.error(
            f"An error occurred while handling {item.__class__.__name__}: {error}",
            exc_info=error,
        )
        embed = ErrorEmbed(
            "錯誤", f"在處理 `{item.__class__.__name__}` 時發生錯誤:\n```py\n{error}\n```"
        )
        try:
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True,
            )
        except discord.InteractionResponded:
            await interaction.followup.send(embed=embed)
        except Exception:
            pass
