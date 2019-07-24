# Ugh I gotta start using notes and shit
import discord
# Red stuffs
from redbot.core import checks, Config, bank, commands
from redbot.core.utils import mod
from redbot.core.utils.chat_formatting import bold, box, inline
import asyncio
import datetime
import random
# League stuffs
import cassiopeia as cass

cass.set_default_region("EUNE")

class Leaguehell(commands.Cog):
    """The League Cog for Hell"""

    def __init__(self, bot):
        self.bot = bot
        default_global = {"leagueapikey": None}
        default_member = {
            "Region": None,
            "Summoner": None,
        }
        default_guild = {
            "db": []
        }
        self.config = Config.get_conf(self, identifier=690430666, force_registration=True)
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)


    @checks.is_owner()
    @commands.command(name="leagueapi")
    async def leagueapi(self, ctx, *, key):
        """Set a key to use the league api"""
        config_boards = await self.config.leagueapikey()
        cass.set_riot_api_key(key)
        await ctx.send(config_boards)

    @commands.command(name="summoner")
    async def summoner(self, ctx, name: str):
        """Use !!summoner <name>\nCurrently works with EUNE only"""
        summ = cass.Summoner(name=name)
        gwith = summ.champion_masteries.filter(lambda cm: cm.level >= 6)
        await ctx.send((cm.champion.name) for cm in gwith)