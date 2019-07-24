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
from cassiopeia import Division, Summoner, Rank, MatchHistory, Champion, Champions, ChampionMastery


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

    @commands.command(name="champs")
    async def champs(self, ctx, name: str):
        """Use !!champs <Summoner name>\nIf the summoner name has a lot of special characters use quotes ("Summoner name").\n\n**Currently works with EUNE only**"""
        usr = ctx.author
        try:
            summ = cass.Summoner(name=name)
            dnname = usr.display_name
            sumname = str(summ.name).capitalize()
            em = discord.Embed(colour=15158332)
            av = usr.avatar_url
            avstr = str(av)
            emdesc = (f"{sumname}'s  champions at level 5+'")
            em.description = emdesc
            em.url = avstr
            em.set_footer(text=(f"Requested by {dnname} | Powered by HELL"), icon_url=avstr)
            Summoner.champion_masteries
            gwith = summ.champion_masteries.filter(lambda cm: cm.level >= 5)
            for cm in gwith:
                chname = cm.champion.name
                cpoints = cm.points
                clvl = cm.level
                cmtokens = cm.tokens
                em.add_field(name=(f"{chname} lvl {clvl}"), value=(f"At {cpoints} points. {cmtokens}"), inline=True)
            await ctx.send(embed=em)
        except:
            await ctx.send(">Shitter's clogged, buddy")
