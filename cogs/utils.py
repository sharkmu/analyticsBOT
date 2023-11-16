from discord.ext import commands

class utils(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot

    @commands.hybrid_command()
    async def sync(self, ctx):
        try:
            synced = await self.bot.tree.sync()
            await ctx.send(f"Successfully synced {len(synced)} command(s)")
        except Exception as e:
            await ctx.send(f"Error while trying to sync: {e}")

    @commands.hybrid_command()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.reload_extension(cog)
            await ctx.send(f"Successfully reloaded {cog}")
        except Exception as e:
            await ctx.send(f"Error while trying to reload: {e}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(utils(bot))