import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import C

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        em = discord.Embed(title=f"<:Checkmark:914194747768315964> Purged {amount} messages", color=discord.Color.purple())
        em.set_footer(text="M1 bot. By Pythonic guy")
        await ctx.send(embed = em)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        em = discord.Embed(title=f"<:Checkmark:914194747768315964> kicked {member.mention} for {reason}", color=discord.Color.purple())
        em.set_footer(text="M1 bot. By Pythonic guy")
        await ctx.send(embed = em)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        em = discord.Embed(title=f"<:Checkmark:914194747768315964> banned {member.mention} for {reason}", color=discord.Color.purple())
        em.set_footer(text="M1 bot. By Pythonic guy")
        await ctx.send(embed = em)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        banned_users= await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                return

def setup(bot):
    bot.add_cog(Moderation(bot))