import typing

import discord
from waifuim import WaifuAioClient, types

from dev.model import BaseView, DefaultEmbed, ErrorEmbed, Inter, translator
from utility.paginator import GeneralPaginator


class TagSelectView(BaseView):
    def __init__(
        self, tags: typing.Dict[str, typing.List[str]], locale: discord.Locale
    ) -> None:
        self.tags = tags
        self.selected_tags: typing.List[str] = []
        self.add_item(
            TagSelect(
                tags["versatile"],
                translator.trans("Select sfw tags...", locale),
                locale,
            )
        )
        self.add_item(
            TagSelect(
                tags["nsfw"], translator.trans("Select nsfw tags...", locale), locale
            )
        )


class TagSelect(discord.ui.Select):
    def __init__(
        self,
        tags: typing.List[str],
        placeholder: str,
        locale: discord.Locale,
    ) -> None:
        super().__init__(
            placeholder=placeholder,
            options=[
                discord.SelectOption(label=translator.trans(tag, locale), value=tag)
                for tag in tags
            ],
            max_values=len(tags),
        )

        self.view: TagSelectView

    async def callback(self, i: discord.Interaction) -> None:
        await i.response.defer()
        self.view.selected_tags.extend(self.values)
        self.view.selected_tags = list(set(self.view.selected_tags))


class SearchImage(discord.ui.Button):
    def __init__(self, label: str) -> None:
        super().__init__(label=label, style=discord.ButtonStyle.primary)

        self.view: TagSelectView

    async def callback(self, i: Inter) -> None:
        await i.response.edit_message(
            embed=DefaultEmbed(translator.trans("Searching...", i.locale))
        )

        wf = WaifuAioClient(session=i.client.session, app_name="Layla")
        images = await wf.search(self.view.selected_tags, many=True)
        if isinstance(images, types.Image):
            images = [images]
        elif isinstance(images, dict):
            return await i.response.edit_message(
                embed=ErrorEmbed(translator.trans("No images found", i.locale))
            )

        embeds: typing.List[discord.Embed] = []
        for image in images:
            embed = DefaultEmbed()
            embed.set_image(url=str(image))
            embeds.append(embed)

        await GeneralPaginator(i, embeds).start(edit=True)
