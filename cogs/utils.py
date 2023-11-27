from discord.ext import commands
from config import config
from database.live_update_database import LiveUpdateDatabase

class utils(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
        self.db = LiveUpdateDatabase()

    @commands.hybrid_command()
    async def sync(self, ctx):
        lang = self.db.get_language(str(ctx.guild.id))
        lang_config = getattr(config, lang[0]) #type: ignore     
        try:
            synced = await self.bot.tree.sync()
            await ctx.send(lang_config["SYNC_COMMANDS_MSG"] + str(len(synced)))
        except Exception as e:
            await ctx.send(lang_config["SYNC_ERROR_MSG"] + str(e))

    @commands.hybrid_command()
    async def reload(self, ctx, *, cog: str):
        lang = self.db.get_language(str(ctx.guild.id))
        lang_config = getattr(config, lang[0]) #type: ignore     
        try:
            await self.bot.reload_extension(cog)
            await ctx.send(lang_config["RELOAD_MSG"] + str(cog))
        except Exception as e:
            await ctx.send(lang_config["RELOAD_ERROR_MSG"] + str(e))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(utils(bot))