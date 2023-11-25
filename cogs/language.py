import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal


class language(commands.Cog): 
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
 
    @app_commands.command(name="language", description="Change the language of the bot. Required permission: administrator")
    @app_commands.default_permissions(administrator=True)
    async def language(self, interaction: discord.Interaction, languages: Literal["English", "Magyar", "Deutsch"]):
        await interaction.response.send_message(f"You choose this: {languages}")

    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(language(bot))