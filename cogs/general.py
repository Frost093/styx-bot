import discord
import random

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

    @commands.command()
    async def frat(self, ctx):
        await ctx.send("Relax pal.")

    @commands.command()
    async def cf(self, ctx):
        if random.random() < 0.5:
            await ctx.send("Heads!")
            return
        await ctx.send("Tails!")

    @commands.command()
    async def dice(self, ctx):
        result = random.randint(1, 6)
        await ctx.send(f"You rolled a {result}.")

    @commands.command(name = "8ball")
    async def _8ball(self, ctx):
        responses = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
        ]
        await ctx.send(random.choice(responses))

    @commands.command()
    async def coinflip(self, ctx, memeber: discord.Member):
        if discord.Forbidden:
            embed = discord.Embed(
                title="Error",
                description="Boop failed. (hint: user dms closed, or bot lacks permission)",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        embed_boop = discord.Embed(
            title="Boop!",
            description=f"Boop! You were booped by {ctx.author.name}!",
            color=discord.Color.green()
        )
        await memeber.send(embed=embed_boop)
        embed = discord.Embed(
            title="Boop Sent",
            description=f"Successfully booped {memeber.display_name} in their DMs!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def time(self, ctx):
        from datetime import datetime
        time = datetime.now()
        embed = discord.Embed(
            title="Current Time",
            description=f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def racism(self, ctx):
        await ctx.send(f"{ctx.author.name} is {random.randint(0, 100)}% racist. No racism allowed!")

    @commands.command()
    async def ai(self, ctx):
        await ctx.send(f"{ctx.author.name} is {random.randint(0, 100)}% AI. AI usage is not allowed!")

async def setup(bot):
    await bot.add_cog(General(bot))