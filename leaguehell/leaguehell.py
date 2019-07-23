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
from .cass import Cass
from cassiopeia import Summoner

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
        await self.config.leagueapikey.set(key)
        await Cass.casskey(key)
        await ctx.send("gj we")

    @commands.command(name="summoner")
    async def summoner(self, ctx, name: str, region: str):
        """Use !!summoner <name> <region>"""
        summoner = Summoner(name=name, region=region)
        sumname = summoner.name
        sumid = summoner.id
        sumaccid = summoner.account_id
        sumlvl = summoner.level
        sumrevdate = summoner.revision_date
        sumico = summoner.profile_icon.image
        em = discord.Embed(colour=15158332)
        emdes = ("Vafli")
        em.description = emdes
        em.set_thumbnail(url=sumico)
        em.add_field(name=(f"{sumname}, level {sumlvl}"), value=(f"ID: {sumid}, Account ID: {sumaccid}, Revision date: {sumrevdate}"))
        em.set_footer(text="Powered by HELL")
        await ctx.send(embed=em)
