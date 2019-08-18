# Libs
import aiohttp
import asyncio
from math import floor, ceil
import datetime
import discord
import re
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
    
    async def cleanhtml(self, stuff):
        cleanr = re.compile('<.*?>')
        clean = re.sub(cleanr, '', stuff)
        return clean

    async def search_leaguename(self, name):
        registered = await self.config.all_members()
        for k in registered:
            for v in registered[k]:
                if name in v:
                    return k
        return "Error"
        