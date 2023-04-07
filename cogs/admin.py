from discord.ext import commands


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="sync")
    async def sync_tree(self, ctx: commands.Context):
        message = await ctx.send("Syncing...")
        await self.bot.tree.sync()
        await message.edit(content="Synced")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))
