import importlib

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

    @commands.is_owner()
    @commands.command(name="reload")
    async def reload_module(self, ctx: commands.Context, module: str):
        message = await ctx.send("Reloading...")
        try:
            importlib.reload(importlib.import_module(module))
        except Exception as e:
            await message.edit(content=f"Failed to reload {module}\n{e}")
            return
        await message.edit(content=f"Reloaded {module} successfully")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))
