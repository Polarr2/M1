import re
import discord
import random
import aiosqlite
from discord.ext import commands
from discord.ext.commands.cooldowns import C
from discord.ext.commands.core import command
async def open_account(member:discord.Member):
        db = await aiosqlite.connect("main.db")
        cursor=await db.cursor()
        await cursor.execute(f"SELECT * FROM economy WHERE member_id = {member.id}")
        result = await cursor.fetchone()

        if result:
            return
        if not result:
            await cursor.execute(f"INSERT INTO economy(member_id, wallet, bank) VALUES(?,?,?)", (member.id, 500, 500))
        
        await db.commit()
        await cursor.close()
        await db.close()


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["bal"], name="balance", brief="Tells you your balance", description="Tells you your balance")
    async def balance(self, ctx, member:discord.Member=None):
        if member is None or member == None:
            member = ctx.author
        
        await open_account(member)

        db = await aiosqlite.connect("main.db")
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM economy WHERE member_id = {member.id}")
        result = await cursor.fetchone()

        em = discord.Embed(description=f"**{member.mention}'s balance**", color=discord.Color.purple())
        em.add_field(name=":dango:  Wallet", value=f"{result[1]}", inline=False)
        em.add_field(name=":bank: Bank", value=f"{result[2]}", inline=False)
        em.set_author(name="dango economy")
        await ctx.send(embed = em)
    
    @commands.command(name="beg", brief="beg for money", description="gives you up to 100 coins")
    async def beg(self, ctx):
        member = ctx.author
        await open_account(member)
        amt = random.randrange(101)
        db = await aiosqlite.connect("main.db")
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM economy WHERE member_id = {member.id}")
        result = await cursor.fetchone()
        await cursor.execute("UPDATE economy SET wallet = ? WHERE member_id = ?", (result[1] + amt, member.id))
        await db.commit()
        await cursor.close()
        await db.close()
        em = discord.Embed(title="Somebody gave you some dango", description=f"A stranger gave you {amt} dango :dango: !", color=discord.Color.purple())
        em.set_author(name="dango economy")
        await ctx.send(embed = em)

    @commands.command(name="withdraw", brief="takes money from the bank", description="takes money from the bank into your wallet")
    async def withdraw(self, ctx, amount = None):
        member = ctx.author
        await open_account(member)
        if amount == None:
            await ctx.send("Please enter an amount.")
            return
        db = await aiosqlite.connect("main.db")
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM economy WHERE member_id = {member.id}")
        result = await cursor.fetchone()

        amount = int(amount)
        if amount>result[2]:
            await ctx.send("You do not have that much dango...")
            return
        if amount<0:
            await ctx.send("Amount must be positive...")
            return
        await cursor.execute("UPDATE economy SET wallet = ? WHERE member_id = ?", (result[1] + amount, member.id))
        await cursor.execute("UPDATE economy SET bank = ? WHERE member_id = ?", (result[2] - amount, member.id))
        await db.commit()
        await cursor.close()
        await db.close()
        em = discord.Embed(title=f"You withdrew {amount} dango :dango:  ", color=discord.Color.purple())
        em.set_author(name="dango economy")
        await ctx.send(embed = em)
    
    @commands.command(aliases=["dep"], name="deposit", brief="puts money into the bank", description="puts money into the bank from your wallet")
    async def deposit(self, ctx, amount = None):
        member = ctx.author
        await open_account(member)
        if amount == None:
            await ctx.send("Please enter an amount.")
            return
        db = await aiosqlite.connect("main.db")
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM economy WHERE member_id = {member.id}")
        result = await cursor.fetchone()

        if amount == "all":
            await cursor.execute("UPDATE economy SET wallet = ? WHERE member_id = ?", (result[1] - int(result[1]), member.id))
            await cursor.execute("UPDATE economy SET bank = ? WHERE member_id = ?", (result[2] + int(result[1]), member.id))
            await db.commit()
            await cursor.close()
            await db.close()
            em = discord.Embed(title=f"You deposited all of your dango :dango:  ", color=discord.Color.purple())
            await ctx.send(embed = em)
        else:
            amount = int(amount)
            if amount>result[2]:
                await ctx.send("You do not have that much dango...")
                return
            if amount<0:
                await ctx.send("Amount must be positive...")
                return
            await cursor.execute("UPDATE economy SET wallet = ? WHERE member_id = ?", (result[1] - amount, member.id))
            await cursor.execute("UPDATE economy SET bank = ? WHERE member_id = ?", (result[2] + amount, member.id))
            await db.commit()
            await cursor.close()
            await db.close()
            em = discord.Embed(title=f"You deposited {amount} dango :dango:  ", color=discord.Color.purple())
            em.set_author(name="dango economy")
            await ctx.send(embed = em)
        
    @commands.command(aliases=["send"])
    async def give(self, ctx, member: discord.Member, amt):
        amt = int(amt)
        if amt>0:
            db = await aiosqlite.connect("main.db")
            cursor = await db.cursor()
            await cursor.execute(f"SELECT * FROM economy WHERE member_id = {member.id}")
            result1 = await cursor.fetchone()
            await cursor.execute("UPDATE economy SET wallet = ? WHERE member_id = ?", (result1[1] + amt, member.id))
            await cursor.execute(f"SELECT * FROM economy WHERE member_id = {ctx.author.id}")
            result2 = await cursor.fetchone()
            await cursor.execute("UPDATE economy SET wallet = ? WHERE member_id = ?", (result2[1] - amt, ctx.author.id))
            await db.commit()
            await cursor.close()
            await db.close()
            em = discord.Embed(title=f"You gave {member} {amt} dango :dango:  ", color=discord.Color.purple())
            em.set_author(name="dango economy")
            await ctx.send(embed = em)

    @commands.command(aliases=["flip"])
    async def coin_flip(self, ctx,bet=None, choise="heads"):
        member = ctx.author
        bet = int(bet)
        options=["heads", "tails"]
        answer = random.choice(options)
        if bet is None:
            await ctx.send("Please choose an amount to bet.")

        
        db = await aiosqlite.connect("main.db")
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM economy WHERE member_id = {member.id}")
        result = await cursor.fetchone()

        if choise is answer:
            await ctx.send(f"you won! you earned {bet} dango!")
            await cursor.execute("UPDATE economy SET wallet = ? WHERE member_id = ?", (result[1] +  bet, ctx.author.id))
            await db.commit()
            await cursor.close()
            await db.close()
        else:
            await ctx.send(f"you lost! you lost {bet} dango!")
            await cursor.execute("UPDATE economy SET wallet = ? WHERE member_id = ?", (result[1] - bet, ctx.author.id))
            await db.commit()
            await cursor.close()
            await db.close()
        
def setup(bot):
    bot.add_cog(Economy(bot))
