import discord
from discord.ext import commands
from pkgutil import iter_modules
from config import config

EXTENSIONS = [module.name for module in iter_modules(['cogs'], prefix='cogs.')]

class Bot(commands.Bot):
    async def setup_hook(self):
        print(config.START_MESSAGE)
        
        for extension in EXTENSIONS:
            await bot.load_extension(extension)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = Bot(command_prefix = config.BOT_PREFIX, intents=intents)

bot.run(config.BOT_TOKEN)