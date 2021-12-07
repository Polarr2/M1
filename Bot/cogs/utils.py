import discord
from discord.interactions import Interaction
import dotenv
import random
import platform
from time import time
from discord.ext import commands
from discord.ext.commands.cooldowns import C
from discord.components import Button, SelectOption
from discord.ext.commands.core import command
from discord.ui import Button, View, Select
from discord.ui.button import button
from os import scandir
import os
dotenv.load_dotenv()
os.chdir("C:\\Users\\Dylan\\Documents\\Projects py\\M¹\\Bot")

class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gamenight(self, ctx,  url=None, *,  game):
        await ctx.defer()
        if not url is None:
            button = Button(label="Join game!", style=discord.ButtonStyle.green, emoji="🎮" , url=url)
        view = View()
        if not url is None:
            view.add_item(button)
        await ctx.send(f"GAME NIGHT! Game: {game}", view=view)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def reload(self, ctx):
            await ctx.send("Reloading cogs")
            for ext in os.listdir("./cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                    except:
                        await ctx.send("Could not reload all extensions.")
    
    @commands.command()
    async def ping(self,ctx):
        await ctx.defer()
        api_start = time()
        msg = await ctx.send("Ping...")
        api_end = time()
        button = Button(label="Invite me!", style=discord.ButtonStyle.green, emoji="<:PythonicGuy:912663763835060224>" , url="https://discord.com/api/oauth2/authorize?client_id=906530431577522228&permissions=8&scope=bot%20applications.commands")
        view = View()
        view.add_item(button)
        em = discord.Embed(title="Pong! :ping_pong: ", color=discord.Color.purple())
        em.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms ")
        em.add_field(name="API", value=f"{str(round((api_end - api_start) * 1000))}ms ")
        em.set_footer(text="M1 bot. By Pythonic guy")
        await ctx.send(embed = em, view=view)

    @commands.command(description="Made by Polar")
    async def about(self,ctx):
        ver = os.getenv("version")
        em = discord.Embed(title="M1", color=discord.Color.purple())
        em.add_field(name="<:py:912664860695867422> Python version", value=f"``{platform.python_version()}``", inline=False)
        em.add_field(name="<:edpy:912747291545309226> Discord.py version", value=f"``{discord.__version__}``", inline=False)
        em.add_field(name="<:m1:912747316212023398> M1 version", value=f"``{ver}``", inline=False)
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Utils(bot))