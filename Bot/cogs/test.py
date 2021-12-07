import discord
from discord.interactions import Interaction
from discord.ui.select import select
import dotenv
import random
import pomice
import re
import platform
from time import time
from discord.ext import commands
from discord.ext.commands.cooldowns import C
from discord.components import Button, SelectOption
from discord.ext.commands.core import command
from discord.ui import Button, View, Select, Item
from discord.ui.button import button
from os import scandir
import os
dotenv.load_dotenv()

class TestView(View):
    def __init__(self, ctx):
        self.ctx = ctx
        self.user = self.ctx.author
        super().__init__(timeout=15)
    
    @button(label="Click me to disable", style=discord.ButtonStyle.blurple)
    async def callback1(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @button(label="Long boi-----------------------", style=discord.ButtonStyle.red, )
    async def callback2(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.label = "I changed!"
        await interaction.response.edit_message(view=self)
        
    @select(placeholder="Select option lol", options=[SelectOption(label="Lol", value="Lol"),SelectOption(label="Lmao", value=":milk: MAYONAISE ON AN ESCALATOR")])
    async def callback3(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected {select.values} lol", ephemeral=True)

class test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test(self, ctx):
        view = TestView(ctx)
        await ctx.send("Test", view=view)
     
  
def setup(bot):
    bot.add_cog(test(bot))
