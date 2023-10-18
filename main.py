import discord
from discord.ext import commands
import os
from pkgutil import iter_modules

EXTENSIONS = [module.name for module in iter_modules(['cogs'], prefix='cogs.')]
TOKEN = os.getenv('TOKEN')

class Bot(commands.Bot):
    async def setup_hook(self):
        print("Bot is starting")
        
        for extension in EXTENSIONS:
            await bot.load_extension(extension)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = Bot(command_prefix = "?", intents=intents)

bot.run(TOKEN)