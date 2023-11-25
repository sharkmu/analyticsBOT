from discord.ext import commands
from config import config

class memberCount(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
    
    @commands.hybrid_command()
    async def members(self, ctx):
        await ctx.send(config.english["TOTAL_MEMBERS_MSG"] + str(ctx.guild.member_count))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(memberCount(bot))