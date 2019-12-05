import aiohttp
import asyncio
from math import floor, ceil
import datetime
import discord
from discord import utils
from redbot.core import checks, Config, bank, commands

class Hslib:
    def __init__(self, bot):
        self.bot = bot
        # Rapidapi
        self.rurl = "https://omgvamp-hearthstone-v1.p.rapidapi.com"
        self.rapi = None
        self.rkey = None
        self.searchcardname = "/cards/search/{}"
        self.card = "/cards/{}"
        self.hsinfo = "/info"
        self.headers = {
            "X-RapidAPI-Host": "omgvamp-hearthstone-v1.p.rapidapi.com",
            "X-RapidAPI-Key": None
        }
        self._session = aiohttp.ClientSession()
        # cdn?

    def cog_unload(self):
        self.__unload()

    async def __unload(self):
        asyncio.get_event_loop().create_task(self._session.close())

    async def _getapikey(self):
        if not self.rkey:
            db = await self.bot.db.api_tokens.get_raw("hsapikey", default=None)
            self.rkey = db["hsapikey"]
            return self.rkey
        else:
            return self.rkey

    async def _updheaders(self):
        if not self.headers["X-RapidAPI-Key"]:
            self.headers["X-RapidAPI-Key"] = await self._getapikey()
            return self.headers
        else:
            return self.headers
    
    async def _rq(self, rq):
        headers = await self._updheaders()
        async with self._session.get(rq, headers=headers) as r:
            return await r.json()

    async def _getcard(self, name):
        rq = self.rurl + self.card.format(name)
        rj = await self._rq(rq)
        return rj

            
