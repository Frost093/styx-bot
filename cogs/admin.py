import discord
import datetime
from config import DEV_IDS, DEV_ID
from collections import defaultdict, deque
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipe_history = defaultdict(lambda: deque(maxlen=100))
        
        #fix to / AttributeError: 'Admin' object has no attribute 'last_msg_author'
        self.last_msg_author = {}
        self.last_msg_content = {}
        self.last_msg_time = {}

    def deny(self):
        return discord.Embed(
            title="Access Denied",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.content.startswith("!"):
            self.snipe_history[message.channel.id].appendleft(
                (message.author, message.content)
            )

    @commands.command()
    async def env(self, ctx):
        if ctx.author.id in DEV_IDS:
            latency = round(self.bot.latency * 1000)
            total_members = ctx.guild.member_count
            server_name = ctx.guild.name
            user_name = ctx.author.name

            embed = discord.Embed(
                title="Test Successful",
                description=f"Server: {server_name} \nLatency: {latency}ms\nTotal Members: {total_members}\nUser: {user_name}",
                color=discord.Color.blue()
            )
        else:
            embed = self.deny()

        await ctx.send(embed=embed)
    @commands.command()
    async def snipe(self, ctx, amount:int = 1):
        if ctx.author.id not in DEV_IDS:
            await ctx.send(embed=self.deny())
            return

        messages = self.snipe_history[ctx.channel.id]

        if 1 <= amount <= len(messages):
            author, content = messages[amount - 1]
            embed = discord.Embed(
                title="Sniped Message",
                description=f"Author: {author.name} \nContent: {content}",
                color=discord.Color.yellow()
            )
        else:
            embed = discord.Embed(
                title="No Sniped Message",
                description="No message has been sniped in this channel.",
                color=discord.Color.red()
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def rm(self, ctx, amount:int = 1):
        if ctx.author.id not in DEV_IDS:
            await ctx.send(embed=self.deny())
            return

        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(embed=discord.Embed(
            title="Messages Deleted",
            description=f"Deleted {len(deleted)} messages.",
            color=discord.Color.green()
        ))

    @commands.command()
    async def srm(self, ctx, amount:int = 1):
        if ctx.author.id not in DEV_IDS:
            await ctx.send(embed=self.deny())
            return
        
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.author.send(embed=discord.Embed(
            title="Silently Deleted Messages",
            description=f"Deleted {len(deleted)} messages.",
            
            color=discord.Color.red(),
        ))
        log_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{log_timestamp} SRM     {ctx.author.name} deleted {len(deleted)} msgs') # log the srm

    @commands.command()
    async def perms(self, ctx):
        if ctx.author.id in DEV_IDS: 
            dev_status = "✅"
        else:
            dev_status = "❌"
            
        if ctx.author.id == DEV_ID:
            dev_id_status = "✅"
        else:
            dev_id_status = "❌"
            
        
        embed = discord.Embed(
            title="Permissions",
            description=f'Username: {ctx.author.name}\n ID: {ctx.author.id}\n\nDEV_IDS: {dev_status}\nDEV_ID: {dev_id_status}',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))