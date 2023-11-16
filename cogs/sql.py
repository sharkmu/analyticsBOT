from discord.ext import commands

class sql(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        print(f"new message: {message}")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"new member: {member.name}")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"member left: {member.name}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(sql(bot))