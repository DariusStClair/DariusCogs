# Libs
import aiohttp
import asyncio
from math import floor, ceil
import datetime
import discord
import re
from typing import Union
# Red stuffs
from redbot.core import checks, Config, bank, commands

class Handler:
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=690430666, force_registration=True)
        self.config = Config.get_conf
        self.regchecks = ["EUNE", "EUW", "NA", "BR", "JP", "KR", "LAN", "OCE", "TR", "RU", "PBE"]
        self.servers = {
            "eune": "eun1",
            "euw": "euw1",
            "na": "na1",
            "br": "br1",
            "jp": "jp1",
            "kr": "kr",
            "lan": "la1",
            "oce": "oc1",
            "tr": "tr1",
            "ru": "ru",
            "pbe": "pbe1"
        }

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

    async def lookup(self, ctx, author, *, search: Union[discord.Member, str] = None):
        #re = {"nick": "None", "region": "eune"}
        ugherror = ">>> \nError"
        if type(search) is discord.Member:
            reg = await self.config.member(search).Name()
            if str(reg) == "None":
                err_register = ">>> Unregistered member. \nThey can register with: \n`!!league setname <name>`"
                return ugherror, err_register
            else:
                searchreg = await self.config.member(search).Region()
                search = reg
        else:
            if str(search) == "None":
                search = await self.config.member(author).Name()
                searchreg = await self.config.member(author).Region()
                if str(search) == "None":
                    err_regauthor = ">>> Whoa, {author.mention}, you haven't registered your league name. \nThat can be done with `!!league setname <name>`"
                    return ugherror, err_regauthor
            elif str(search) != "None":
                if len(search.split()) > 1:
                    searchlast = search.split()[-1]
                    searchlastl = searchlast.lower()
                    searchlastc = searchlast.upper()
                    if searchlastc in self.regchecks:
                        searchreg = self.servers[searchlastl]
                        searchcut = search.rsplit(" ", 1)[0]
                        search = searchcut
            else:
                search = await self.config.member(author).Name()
                searchreg = await self.config.member(author).Region()
        if str(search) == "None":
            err_horseshit = ">>> Well horseshit, that person hasn't set their league name."
            return ugherror, err_horseshit
        else:
            return search, searchreg
    
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
    
    #def cog_unload(self):
    #    self.bot.loop.create_task(self.session.close())