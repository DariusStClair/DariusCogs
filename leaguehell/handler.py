# Libs
import aiohttp
import asyncio
from math import floor, ceil
import datetime
# Red stuffs
from redbot.core import checks, Config, bank, commands

class Handler:
    def __init__(self, bot):
        self.bot = bot
        Config.get_conf(None, identifier=690430666, cog_name="Leaguehell")
