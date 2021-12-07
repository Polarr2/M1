from typing import AsyncContextManager
import discord
import dotenv
import random
import platform
from discord.ext import commands
from discord.ext.commands.cooldowns import C
from discord.components import Button
from discord.ext.commands.core import command
from discord.ui import Button, View
from discord.ui.button import button
from datetime import datetime
from os import scandir
import asyncio
import os
dotenv.load_dotenv()
os.chdir("C:\\Users\\Dylan\\Documents\\Projects py\\M¹\\Bot")

class listen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="<:Xmark:914194747537625088> Error.",description="<:Pending:914194747550208010> Oh fiddlesticks, you do not have the correct permissions." , color=discord.Color.purple())
            await ctx.send(embed = em)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"running on {discord.__version__} {discord.version_info.releaselevel}")
        start_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"[{start_time}]")
        print(f"logged in as {self.bot.user}")


async def loop(bot):
    await bot.wait_until_ready()

    while not bot.is_closed():
        await bot.change_presence(activity=discord.activity.Game(f" on {len(bot.guilds)} guilds"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.activity.Game(">>help"))
        await asyncio.sleep(10)


def setup(bot):
    bot.loop.create_task(loop(bot))
    bot.add_cog(listen(bot))