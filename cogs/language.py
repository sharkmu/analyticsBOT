import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal
from database.live_update_database import LiveUpdateDatabase
from config import config


class language(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
        self.db = LiveUpdateDatabase()
 
    @app_commands.command(name="language", description="Change the language of the bot. Required permission: administrator")
    @app_commands.default_permissions(administrator=True)
    async def language(self, interaction: discord.Interaction, languages: Literal["english", "magyar", "deutsch"]):
        lang = self.db.get_language(str(interaction.guild_id))
        lang_config = getattr(config, lang[0]) #type: ignore       
        try:
            self.db.update_language(str(interaction.guild_id), languages)
            lang = self.db.get_language(str(interaction.guild_id))
            await interaction.response.send_message(lang_config["UPDATE_LANG_MSG"] + languages)
        except Exception as e:
            conf_lang = lang_config["UPDATE_LANG_ERROR_MSG"]
            await interaction.response.send_message(f"{conf_lang}`{e}`")
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(language(bot))