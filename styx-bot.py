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
async def marco(ctx):  #basic ping
    await ctx.send("Polo!")

@bot.command()
async def env(ctx): #test for env info
    FROST_DC_ID = 1206044443766034522 #main dev ##could  be swaped for owner, ctx.owner##
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
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Access Denied",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        description=f"{latency}ms",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

bot.run(TOKEN)  # Hidden for security reasons