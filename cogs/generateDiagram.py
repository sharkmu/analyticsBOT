from discord.ext import commands
from config import config
from database.live_update_database import LiveUpdateDatabase
from logic.diagram_generation import DiagramLogic
import discord

from io import BytesIO

class generateDiagram(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
        self.db = LiveUpdateDatabase()
        self.diagram = DiagramLogic()
    
    @commands.hybrid_command()
    async def graph(self, ctx):
        lang = self.db.get_language(ctx.guild.id, False)
        lang_config = getattr(config, lang[0]) #type: ignore

        try: 
            fig = self.diagram.generate(ctx.guild.id, ctx.author.id)

            buffer = BytesIO()
            fig.savefig(buffer, format="png")
            buffer.seek(0)
            file = discord.File(buffer, filename="image.png")
            
            await ctx.send(file=file)
        
        except Exception as e:
            print(e)


        #await ctx.send(lang_config["TOTAL_BANS_MSG"] + str(""))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(generateDiagram(bot))