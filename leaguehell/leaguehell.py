# Ugh I gotta start using notes and shit
import discord
# Red stuffs
from redbot.core import checks, Config, bank, commands
from redbot.core.utils import mod
from redbot.core.utils.chat_formatting import bold, box, inline
# Libs
import aiohttp
import asyncio
import datetime
import random
# League stuffs
from .leaguelib import Leaguelib

regchecks = ["EUNE", "EUW", "NA"]

def apikeycheck():
    async def predicate(ctx):
        key = await ctx.bot.db.api_tokens.get_raw("leaguehell", default=None)
        result = True if key["leagueapikey"] else False
        if not result and ctx.invoked_with in dir(ctx.bot.get_cog("Leaguehell")):
            await ctx.send("Yo, api key gotta be set first with the 'leagueapi <key>' command")
        return result
    return commands.check(predicate)

class Leaguehell(commands.Cog):
    """The League Cog for Hell"""

    def __init__(self, bot):
        self.bot = bot
        self.lib = Leaguelib(bot)
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
        await self.bot.db.api_tokens.set_raw("leaguehell", value={'leagueapikey': key})
        await ctx.send("gg wp")

    @checks.is_owner()
    @commands.command(name="leakapi")
    async def leakapi(self, ctx):
        """Leaks your api key. Gj."""
        db = await self.bot.db.api_tokens.get_raw("leaguehell", default=None)
        await ctx.send(db["leagueapikey"])

    @commands.command(name="champs", aliases=["champions"])
    @apikeycheck()
    async def champs(self, ctx, name: str, *, region=None):
        """Use !!champs <name> [region]\nIf the summoner name has a lot of special characters use quotes ("Summoner name").\n\n**Valid regions are BR / EUNE / EUW / JP / KR / LAN / LAS / NA / OCE / TR / RU. \nIf no [region] is specified it defaults to EUNE.**"""
        usr = ctx.author 
        if region is None:
            xreg = "EUNE"
            await ctx.send(f"> DEBUG: Reg is set as: ({xreg}) = ({region})")
            pass
        elif region.upper() in regchecks:
            xreg = region.upper()
            await ctx.send(f"> DEBUG: Reg is set as: ({xreg}) = ({region})")
            pass
        else:
            xreg = region.upper()
            await ctx.send(f"> Invalid region ({xreg}).\n> Valid regions are EUNE / EUW / NA for now. \n> If no [region] is specified it defaults to EUNE.")
            return
        try:
            elo = await self.lib.get_elo(xreg, name)
            dnname = usr.display_name
            sumname = str(name).capitalize()
            em = discord.Embed(colour=15158332)
            av = usr.avatar_url
            avstr = str(av)
            emdesc = (f"{dnname} a.k.a. {sumname}'s  champions at level 6 and above in {xreg} (up to 10):")
            em.description = emdesc
            em.url = avstr
            total = await self.lib.mastery_score(xreg, name)
            em.set_footer(text=(f"ELO: {elo} | Total mastery points: {total} | Powered by HELL"), icon_url=avstr)
            champs = await self.lib.top_champs(xreg, name)
            temp = 0
            for i in champs:
                chname = await self.lib.get_champ_name(str(i["championId"]))
                clvl = i["championLevel"]
                cpoints = i["championPoints"]
                cchest = i["chestGranted"]
                if cchest is True:
                    chest = "Yes"
                else:
                    chest = "No"
                cmtokens = "__*WIP*__"
                cmlp = "__*WIP*__"
                em.add_field(name=(f"{chname}"), value=(f"At **{cpoints}** points.\nLevel **{clvl}**.\n**{cmtokens}** tokens.\nChest granted? **{chest}**.\nLast played: **{cmlp}**."), inline=True)
                if temp >= 10:
                    break
                await asyncio.sleep(0.5)
            await ctx.send(embed=em)
        except:
            await ctx.send("> Shitter's clogged, buddy. \n> Yes, that's an error.\n> **Protip: If your summoner name has special characters (ó / Ø / Θ etc) put it in quotes like \"TóóΘpki\".**")

    @commands.command(name="lhtest")
    async def lhtest(self, ctx, name, xreg):
        author = ctx.author
        if xreg.lower() == "none":
            xreg = "eun1"
            return xreg
        uhelo = await self.lib.get_ranked(name, xreg)
        propername = await self.lib.get_prname(name, xreg)
        #for i in uhelo:
        #    await ctx.send(i)
        #    await asyncio.sleep(0.5)
        em = discord.Embed(colour=15158332)
        em.set_footer(text=f"Powered by HELL | Requested by {author} | version: 0.00")
        em.description = (f"{author}'s shit:'")
        #temp = 0
        for i in uhelo:
            queuetype = i["queueType"]
            wins = i["wins"]
            losses = i["losses"]
            tier = i["tier"]
            rank = i["rank"]
            leaguepnts = i["leaguePoints"]
            em.add_field(name=(f"{queuetype}"), value=(f"{tier} {rank} :white_small_square: {leaguepnts} LP :white_small_square: Wins/losses: {wins}/{losses}"), inline=False)
            await asyncio.sleep(0.5)
        await ctx.send(embed=em)
            
        #await ctx.send(f"> DEBUG: {uhelo}")