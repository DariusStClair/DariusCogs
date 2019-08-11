# Libs
import aiohttp
import asyncio
from math import floor, ceil
import datetime
import discord
# Red stuffs
from redbot.core import checks, Config, bank, commands

class Handler:
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=690430666, force_registration=True)
        self.config = Config.get_conf
    async def check_modadmin(self, author: discord.Member):
        guild = author.guild
        if author == guild.owner:
            return True
        if await self.bot.is_owner(author):
            return True
        if await self.bot.is_admin(author):
            return True
        if await self.bot.is_mod(author):
            return True
        return False
    
    async def get_leaguename(self, name: discord.Member=None):
            re = await self.config.member(name).Name()
            return re
    