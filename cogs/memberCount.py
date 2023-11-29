from discord.ext import commands
from config import config
from database.live_update_database import LiveUpdateDatabase

class memberCount(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
        self.db = LiveUpdateDatabase()
    
    @commands.hybrid_command()
    async def members(self, ctx):
        lang = self.db.get_language(str(ctx.guild.id), False)
        lang_config = getattr(config, lang[0]) #type: ignore     
        await ctx.send(lang_config["TOTAL_MEMBERS_MSG"] + str(ctx.guild.member_count))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(memberCount(bot))