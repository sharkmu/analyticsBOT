import discord
from discord.ext import commands
import os

TOKEN = os.getenv('TOKEN')

class Bot(commands.Bot):
    async def setup_hook(self):
        print("Bot is starting")
        await self.load_extension("cogs.memberCount")
        await self.load_extension("cogs.bans")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = Bot(command_prefix = "?", intents=intents)

bot.run(TOKEN)