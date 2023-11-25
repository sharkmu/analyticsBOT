from discord.ext import commands
from config import config

class utils(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot

    @commands.hybrid_command()
    async def sync(self, ctx):
        try:
            synced = await self.bot.tree.sync()
            await ctx.send(config.english["SYNC_COMMANDS_MSG"] + str(len(synced)))
        except Exception as e:
            await ctx.send(config.english["SYNC_ERROR_MSG"] + str(e))

    @commands.hybrid_command()
    async def reload(self, ctx, *, cog: str):
        try:
            await self.bot.reload_extension(cog)
            await ctx.send(config.english["RELOAD_MSG"] + str(cog))
        except Exception as e:
            await ctx.send(config.english["RELOAD_ERROR_MSG"] + str(e))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(utils(bot))