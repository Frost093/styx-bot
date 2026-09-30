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

@bot.command()
async def marco(ctx):
    await ctx.send("Polo!")
bot.run(TOKEN)  # Hidden for security reasons

