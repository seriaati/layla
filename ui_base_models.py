import discord
from utility import error_embed


async def global_error_handler(
    i: discord.Interaction, e: Exception | discord.app_commands.AppCommandError
):
    if isinstance(e, discord.app_commands.errors.CheckFailure):
        return
    if hasattr(e, "code") and e.code in [10062, 10008, 10015]:
        embed = error_embed()
        embed.set_author(name="操作逾時，請再試一次")
    else:
        embed = error_embed()
        embed.description += f"\n```{e}```"
        embed.set_author(
            name="出錯了",
            icon_url=i.user.display_avatar.url,
        )
        embed.set_thumbnail(url="https://i.imgur.com/Xi51hSe.gif")
    view = discord.ui.View()
    view.add_item(
        discord.ui.Button(
            label="支援伺服器",
            url="https://discord.gg/ryfamUykRw",
            emoji="<:discord_icon:1032123254103621632>",
        )
    )

    try:
        await i.response.send_message(
            embed=embed,
            ephemeral=True,
            view=view,
        )
    except discord.errors.InteractionResponded:
        await i.followup.send(
            embed=embed,
            ephemeral=True,
            view=view,
        )
    except discord.errors.NotFound:
        pass


class BaseView(discord.ui.View):
    async def interaction_check(self, i: discord.Interaction) -> bool:
        if not hasattr(self, "author"):
            return True
        if self.author.id != i.user.id:
            await i.response.send_message(
                embed=error_embed().set_author(
                    name="這不是你的操作視窗",
                    icon_url=i.user.display_avatar.url,
                ),
                ephemeral=True,
            )
        return self.author.id == i.user.id

    async def on_error(self, i: discord.Interaction, e: Exception, item) -> None:
        await global_error_handler(i, e)

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        try:
            await self.message.edit(view=self)
        except:
            pass
