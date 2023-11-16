from discord.ext import commands
from database.classes import GuildData, UserData, Guild, DiscordBotDatabase

class sql(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
        self.db = DiscordBotDatabase()

    def db_add_guild(self, gId: str, guild):
        self.db.add_or_update_guild(
            guild_id= gId,
            guild_data=GuildData(
                member_count=guild.member_count,
                user_ban_count=0, # TODO
                chat_count=0, # don't edit this
            )
        )
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.db_add_guild(guild.id, guild)

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