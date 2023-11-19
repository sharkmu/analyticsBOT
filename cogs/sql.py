from discord.ext import commands
from database.classes import GuildData, UserData, Guild, DiscordBotDatabase

class sql(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
        self.db = DiscordBotDatabase(None)

    async def db_add_guild(self, gId: str, guild):
        banCount = 0
        async for i in guild.bans(limit=100000):
            banCount += 1
        print(banCount)
        self.db.add_or_update_guild(
            guild_id= gId,
            guild_data_arg=GuildData(
                member_count=guild.member_count,
                user_ban_count=banCount,
                chat_count=0,
            )
        )
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.db_add_guild(guild.id, guild)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        print(f"new message: {message}")

        # test - will remove it
        db_result = self.db.get_guild(guild_id="1162767244808425583")
        print(db_result)
        # ---
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"new member: {member.name}")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"member left: {member.name}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(sql(bot))