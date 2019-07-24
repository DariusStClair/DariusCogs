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
from cassiopeia import Division, Summoner, Rank, MatchHistory, Champion, Champions, ChampionMastery, Settings

regchecks = ['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'TR', 'RU']
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

    @commands.command(name="champs", aliases=["champions"])
    async def champs(self, ctx, name: str, *, region=None):
        """Use !!champs <name> [region]\nIf the summoner name has a lot of special characters use quotes ("Summoner name").\n\n**Valid regions are BR / EUNE / EUW / JP / KR / LAN / LAS / NA / OCE / TR / RU. \nIf no [region] is specified it defaults to EUNE.**"""
        usr = ctx.author 
        if region is None:
            xreg = "EUNE"
            #await ctx.send(f">DEBUG: Reg is set as: ({xreg}) = ({region})")
            pass
        elif region.upper() in regchecks:
            xreg = region.upper()
            #await ctx.send(f">DEBUG: Reg is set as: ({xreg}) = ({region})")
            pass
        else:
            xreg = region.upper()
            await ctx.send(f">Invalid region ({xreg}).\n>Valid regions are BR / EUNE / EUW / JP / KR / LAN / LAS / NA / OCE / TR / RU. \n>If no [region] is specified it defaults to EUNE.")
            return
        try:
            summ = cass.Summoner(name=name, region=xreg)
            dnname = usr.display_name
            sumname = str(summ.name).capitalize()
            em = discord.Embed(colour=15158332)
            av = usr.avatar_url
            avstr = str(av)
            emdesc = (f"{sumname}'s  champions at level 6 and above in {xreg}:")
            em.description = emdesc
            em.url = avstr
            em.set_footer(text=(f"Requested by {dnname} | Powered by HELL"), icon_url=avstr)
            Summoner.champion_masteries
            gwith = summ.champion_masteries.filter(lambda cm: cm.level >= 6)
            for cm in gwith:
                chname = cm.champion.name
                cpoints = cm.points
                clvl = cm.level
                cchest = cm.chest_granted
                if cchest is True:
                    chest = "Yes"
                else:
                    chest = "No"
                cmtokens = cm.tokens
                cmlpx = str(cm.last_played)
                cmlp = cmlpx[:10]
                em.add_field(name=(f"{chname}"), value=(f"At **{cpoints}** points.\nLevel **{clvl}**.\n**{cmtokens}** tokens.\nChest granted? **{chest}**.\nLast played: **{cmlp}**."), inline=True)
            await ctx.send(embed=em)
        except:
            await ctx.send(">Shitter's clogged, buddy. \n>Yes, that's an error.\n>**Protip: If your summoner name has special characters (ó / Ø / Θ etc) put it in quotes like \"TóóΘpki\".**")

    @commands.command(name="lolprofile", aliases=["lprofile"])
    async def lolprofile(self, ctx, name: str, *, region=None):
        """Vafli"""
        #usr = ctx.author 
        if region is None:
            xreg = "EUNE"
            pass
        elif region.upper() in regchecks:
            xreg = region.upper()
            pass
        else:
            xreg = region.upper()
            await ctx.send(f">Invalid region ({xreg}).\n>Valid regions are BR / EUNE / EUW / JP / KR / LAN / LAS / NA / OCE / TR / RU. \n>If no [region] is specified it defaults to EUNE.")
            return
        #try:
        summ = cass.Summoner(name=name, region=xreg)
        vafid = summ.account_id 
        vaflgs = summ.leagues
        vaflgsp = summ.league_positions
        #vaflast = summ.rank_last_season
        vaflvl = summ.level
        vafranks = summ.ranks
        await ctx.send(f"summ:\n {summ}\n", f"vafid:\n {vafid}\n", f"vaflgs:\n {vaflgs}\n", f"vaflgsp:\n {vaflgsp}\n")
        await ctx.send(f"vaflvl:\n {vaflvl}\n", f"vafranks:\n {vafranks}")
        #except:
            #await ctx.send(">Shitter's clogged, buddy. \n>Yes, that's an error.\n>**Protip: If your summoner name has special characters (ó / Ø / Θ etc) put it in quotes like \"TóóΘpki\".**")
