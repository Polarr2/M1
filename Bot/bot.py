import discord
import aiosqlite
import dotenv
import asyncio
import os
import math
import platform

from asyncio.tasks import wait
from discord.ext import commands
from discord import activity
from discord import components
from discord.components import Button
from discord.ui import Button, View
from discord.ext.commands import context
from discord.ext.commands.core import command, cooldown

os.chdir("C:\\Users\\Dylan\\Documents\\Projects py\\M¹\\Bot")
dotenv.load_dotenv()


class M1(commands.AutoShardedBot):
    def __init__(self):
        
        super().__init__(
            ">>",
            description="Nothing to see here!",
            intents=discord.Intents().all(),
            slash_commands=True,
            case_insensitive=True,
            strip_after_prefix=True,
            help_command=commands.MinimalHelpCommand(),
        )

    async def setup(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                M1.load_extension(name=f"cogs.{filename[:-3]}", self=self)