from os import scandir
import discord
import random
import aiohttp
from discord.ext import commands
from discord.ext.commands.cooldowns import C
from discord.components import Button
from discord.ui import Button, View
from discord.ui.button import button

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cool(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        em = discord.Embed(title="Coolness meter :thermometer:", description=f"{member} is {random.randrange(101)}% cool", color=discord.Color.purple())
        await ctx.send(embed = em)

    @commands.command()
    async def love(self, ctx, member1 : discord.Member = None, member2 : discord.Member = None):
        if member1 is None:
            member = ctx.author
        if member2 is None:
            await ctx.send("Who should I pair you with? (Syntax = love <member1> <member2>")
        em = discord.Embed(title="Love meter :love_letter:", description=f"{member1} {random.randrange(101)}% loves {member2}", color=discord.Color.purple())
        await ctx.send(embed = em)

    @commands.command(name="pp")
    async def pp(self, ctx, person: discord.Member = commands.Option(description="Who's PP size do you want to measure?", default=None)):
        person = person or ctx.author
        size = '8' + ''.join(["=" for _ in range(random.randrange(0,20))]) + 'D'
        embed = discord.Embed(title="PP Size", description=f"{person.mention}'s pp size is\n{size}", color=discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.command(name="rps")
    async def rps(self, ctx):
        choices = ["rock", "paper", "scissors"]
        rock = Button(label="Rock", style=discord.ButtonStyle.green)
        paper = Button(label="Paper", style=discord.ButtonStyle.green)
        scissors = Button(label="Scissors", style=discord.ButtonStyle.green)

        async def rock_chosen(interaction):
            answer = random.choice(choices)
            if answer == "paper":
                await interaction.response.send_message(" I chose paper. You lose!")
            if answer == "scissors":
                await interaction.response.send_message(" I chose scissors. You win!")
            if answer == "rock":
                await interaction.response.send_message(" I chose rock. Tie!")

        async def paper_chosen(interaction):
            answer = random.choice(choices)
            if answer == "paper":
                await interaction.response.send_message(" I chose paper. Tie!")
            if answer == "scissors":
                await interaction.response.send_message(" I chose scissors. You lose!")
            if answer == "rock":
                await interaction.response.send_message(" I chose rock. You win!")

        async def scissors_chosen(interaction):
            answer = random.choice(choices)
            if answer == "paper":
                await interaction.response.send_message(" I chose paper. You win!")
            if answer == "scissors":
                await interaction.response.send_message(" I chose scissors. Tie!")
            if answer == "rock":
                await interaction.response.send_message(" I chose rock. You lose!")
            
        rock.callback = rock_chosen
        paper.callback = paper_chosen
        scissors.callback = scissors_chosen
        view = View()
        view.add_item(rock)
        view.add_item(paper)
        view.add_item(scissors)
        message = await ctx.send("Rock, Paper, Scissors!",view=view)
    
    @commands.command()
    async def maid(self, ctx: commands.Context) -> discord.Message:
        async with aiohttp.ClientSession() as session:
            img = await session.get('https://api.waifu.im/sfw/maid/')
            image = await img.json()

        embed = discord.Embed(title="Anime", color=discord.Color.purple())
        embed.set_image(url=image['images'][0]['url'])
        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx: commands.Context) -> discord.Message:
        async with aiohttp.ClientSession() as session:
            image = await session.get('https://some-random-api.ml/animal/cat')
            image = await image.json()

        embed = discord.Embed(title="Cat", color=discord.Color.purple())
        embed.set_image(url=image['image'])
        await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx: commands.Context) -> discord.Message:
        async with aiohttp.ClientSession() as session:
            image = await session.get('https://some-random-api.ml/animal/dog')
            image = await image.json()

        embed = discord.Embed(title="Dog", color=discord.Color.purple())
        embed.set_image(url=image['image'])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))