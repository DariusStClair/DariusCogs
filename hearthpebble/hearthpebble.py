import discord
from discord.utils import get
# Red stuffs
from redbot.core import checks, Config, bank, commands
from redbot.core.utils import mod
from redbot.core.utils.menus import menu, start_adding_reactions, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import bold, box, inline
# Libs
import aiohttp
import asyncio
import datetime
import random
import re
from typing import Union
# HS stuffs
from .hslib import Hslib

vversion = "version: 0.00"
deffooter = f"Powered by Entropy | {vversion}"

def apikeycheck():
    async def predicate(ctx):
        key = await ctx.bot.db.api_tokens.get_raw("hearthpebble", default=None)
        try:
            result = True if key["hsapikey"] else False
        except:
            result = False
        if not result and ctx.invoked_with in dir(ctx.bot.get_cog("Hearthpebble")):
            await ctx.send("Yo, api key gotta be set first with the 'hsapikey <key>' command")
        if ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=ctx.bot.user.id)).add_reactions:
            return result
        else:
            raise commands.ReactionsCheckFailure(message="I got no permissions to add reactions")
    return commands.check(predicate)

class Hearthpebble(commands.Cog):
    """Yet another shitty Hearthstone Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.lib = Hslib(bot)
        default_global = {"hsapikey": None}
        self.config = Config.get_conf(self, identifier=698731666, force_registration=True)
        self.config.register_global(**default_global)

    @checks.is_owner()
    @commands.command(name="hsapikey")
    async def hsapikey(self, ctx, *, key):
        """Set a key to use the Hearthpebble commands"""
        await self.bot.db.api_tokens.set_raw("hsapikey", value={'hsapikey': key})
        await ctx.send(">>> Easy.")

    @commands.group(name="hs", no_pm=True)
    async def hs(self, ctx):
        """Various Hearthstone commands"""
        pass

    @hs.command(pass_context=True, no_pm=True)
    async def card(self, ctx, *, name):
        """Search for a card"""
        res = await self.lib._getcard(name)
        await ctx.send(res)