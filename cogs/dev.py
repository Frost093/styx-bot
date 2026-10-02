import discord

from config import DEV_ID
from discord.ext import commands

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def deny(self):
        return discord.Embed(
            title="Access Denied",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        )

    @commands.command()
    async def dev_test(self, ctx):
        if ctx.author.id in DEV_ID:
            embed = discord.Embed(
                title="Dev Test Successful",
                description="This is a test command for developers.",
                color=discord.Color.green()
            )
        else:
            embed = self.deny()
        await ctx.send(embed=embed)

    @commands.command()
    async def dev_embed(self, ctx, title: str, description: str, color: str):
        if ctx.author.id in DEV_ID:
            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.from_str(color)
            )
        else:
            embed = self.deny()
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Dev(bot))