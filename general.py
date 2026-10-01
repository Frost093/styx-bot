import discord
from discord.ext import commands
from datetime import datetime, timezone

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def marco(self, ctx):
        await ctx.send("Polo!")

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            description=f"{latency}ms",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def uptime(self,ctx):
        delta = datetime.now(timezone.utc) - self.bot.launch_time
        if delta.days == 0:
            delta_str = f"{delta.seconds//3600} hours, {(delta.seconds//60)%60} minutes, and {delta.seconds%60} seconds"
        else:
            delta_str = f"{delta.days} days, {delta.seconds//3600} hours, {(delta.seconds//60)%60} minutes, and {delta.seconds%60} seconds"

        embed = discord.Embed(
            title="Bot Uptime",
            description=f"{delta_str}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))