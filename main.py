import datetime
import os
import discord
import random
import config

from discord.ext import commands, tasks
from dotenv import load_dotenv #fun tokens
load_dotenv()
TOKEN =  os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

@tasks.loop(hours=1) # run every hour for the "FIRE UP THE:" message
async def hourly_task():
    channel = bot.get_channel(config.CHANNEL_ID) #oohhhhhhhh
    if channel:
        if random.random() < 0.5:
            embed = discord.Embed(
                title="FIRE UP THE:",
                description="Notebooks!",
                color=discord.Color.orange()
            )
            await channel.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="FIRE UP THE:",
            description="Chromebooks!",
            color=discord.Color.red()
        )
        await channel.send(embed=embed)
    else:
        print("Channel not found.")

@hourly_task.before_loop
async def before_send_hourly_message():
    await bot.wait_until_ready()
    print("Starting the hourly message loop...")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.launch_time = datetime.datetime.now(datetime.timezone.utc)
    print(f'Current time (UTC): {bot.launch_time}')

    #wait for loading cogs
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.admin")
    print("Cogs loaded successfully.")

    if not hourly_task.is_running():
        hourly_task.start()

bot.run(TOKEN)