import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal
from database.live_update_database import LiveUpdateDatabase


class language(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
        self.db = LiveUpdateDatabase()
 
    @app_commands.command(name="language", description="Change the language of the bot. Required permission: administrator")
    @app_commands.default_permissions(administrator=True)
    async def language(self, interaction: discord.Interaction, languages: Literal["english", "magyar", "deutsch"]):
        try:
            self.db.update_language(str(interaction.guild_id), languages)
            await interaction.response.send_message(f"You successfully updated the language to this: {languages}")
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong, try again later! Error: `{e}`")
        print(self.db.get_language(str(interaction.guild_id)))
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(language(bot))