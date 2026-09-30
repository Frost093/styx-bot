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

#var
last_msg_author = {}
last_msg_content = {}
last_msg_time = {}

#events
@bot.event
async def on_message(message):
#stores last msg
    if message.author.bot: #no snipe bot msgs
        return
    #store last msg
    if not message.content.startswith("!"):
        last_msg_author[message.channel.id] = message.author
        last_msg_content[message.channel.id] = message.content
        last_msg_time[message.channel.id] = message.created_at

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.launch_time = datetime.now(timezone.utc)
    print(f'Current time: {bot.launch_time}')

#commands
def deny():
    return discord.Embed(
        title="Access Denied",
        description="You do not have permission to use this command.",
        color=discord.Color.red()
    )
@bot.command()
async def uptime(ctx):
    delta = datetime.now(timezone.utc) - bot.launch_time
    if delta.days == 0:
        delta = f"{delta.seconds//3600} hours, {(delta.seconds//60)%60} minutes, and {delta.seconds%60} seconds"
    else:
        delta = f"{delta.days} days, {delta.seconds//3600} hours, {(delta.seconds//60)%60} minutes, and {delta.seconds%60} seconds"
    
    embed = discord.Embed(
        title="Bot Uptime",
        description=f"{delta}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@bot.command()
async def marco(ctx):  #basic ping
    await ctx.send("Polo!")

@bot.command()
async def env(ctx): #test for env info
    FROST_DC_ID = 1206044443766034522 #main dev ##could  be swaped for owner, ctx.guild.owner##
    JAHU_DC_ID = 1410475638879555675 #owner
    if ctx.author.id  ==  FROST_DC_ID or ctx.author.id == JAHU_DC_ID:
        latency = round(bot.latency * 1000)
        total_members = ctx.guild.member_count
        server_name = ctx.guild.name
        user_name = ctx.author.name

        embed = discord.Embed(
            title="Test Successful",
            description=f"Server: {server_name} \nLatency: {latency}ms\nTotal Members: {total_members}\nUser: {user_name}",
            color=discord.Color.blue()
        )
        
    else:
        embed = deny()
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        description=f"{latency}ms",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
async def snipe(ctx): #snipes msgs so they cant be deleted (useful for moderation)
    FROST_DC_ID = 1206044443766034522 #main dev ##could  be swaped for owner, ctx.guild.owner##
    JAHU_DC_ID = 1410475638879555675 #owner
    
    author = last_msg_author.get(ctx.channel.id)
    content = last_msg_content.get(ctx.channel.id)
    time = last_msg_time.get(ctx.channel.id)

    if ctx.author.id  ==  FROST_DC_ID or ctx.author.id == JAHU_DC_ID:
        if author and content:
            embed = discord.Embed(
                title="Sniped Message",
                description=f"Author: {author.name} \nContent: {content} \nTime: {time}",
                color=discord.Color.yellow()
            )
        else:
            embed = discord.Embed(
                title="No Sniped Message",
                description="No message has been sniped in this channel.",
                color=discord.Color.red()
            )
    else:
        embed = deny()

    await ctx.send(embed=embed)
    
bot.run(TOKEN)  # Hidden for security reasons