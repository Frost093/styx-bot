import aioconsole
import discord 

from config import DEV_ID
from discord.ext import commands
from discord.ext import tasks

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.console_talk.start()

    def deny(self):
        return discord.Embed(
            title="Access Denied",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        )

    @tasks.loop(seconds=0.1)
    async def console_talk(self):
        await self.bot.wait_until_ready()

    # Target channel ID where you want your terminal messages to go
    # Change this to your preferred channel
        target_channel_id = 1552640092328296580
        channel = self.bot.get_channel(target_channel_id)

        if channel:
        # Asynchronously wait for you to type something in your computer terminal and hit Enter
            message = await aioconsole.ainput("Type to chat through bot: ")
            if message.strip():
                await channel.send(message)

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