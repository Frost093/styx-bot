from datetime import datetime, timezone
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv #fun tokens
load_dotenv()
TOKEN =  os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.launch_time = datetime.now(timezone.utc)
    print(f'Current time (UTC): {bot.launch_time}')

    #wait for loading cogs
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.admin")
    print("Cogs loaded successfully.")

bot.run(TOKEN)