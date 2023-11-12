from discord.ext import commands

class sql(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        print(f"new message: {message}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(sql(bot))