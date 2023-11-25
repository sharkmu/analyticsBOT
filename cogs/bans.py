from discord.ext import commands
from config import config

class bans(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
    
    @commands.hybrid_command()
    async def bans(self, ctx):
        banCount = 0
        async for entry in ctx.guild.bans(limit=None):
            banCount += 1
        await ctx.send(config.english["TOTAL_BANS_MSG"] + str(banCount))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(bans(bot))