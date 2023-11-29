from discord.ext import commands
from config import config
from database.live_update_database import LiveUpdateDatabase

class bans(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
        self.db = LiveUpdateDatabase()
    
    @commands.hybrid_command()
    async def bans(self, ctx):
        lang = self.db.get_language(ctx.guild.id, False)
        banCount = 0
        async for entry in ctx.guild.bans(limit=None):
            banCount += 1
        lang_config = getattr(config, lang[0]) #type: ignore
        await ctx.send(lang_config["TOTAL_BANS_MSG"] + str(banCount))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(bans(bot))