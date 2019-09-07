# Ugh I gotta start using notes and shit
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
# League stuffs
from .leaguelib import Leaguelib
from .handler import Handler

vversion = "version: 0.05b"
allregistered = []

def apikeycheck():
    async def predicate(ctx):
        key = await ctx.bot.db.api_tokens.get_raw("leaguehell", default=None)
        try:
            result = True if key["leagueapikey"] else False
        except:
            result = False
        if not result and ctx.invoked_with in dir(ctx.bot.get_cog("Leaguehell")):
            await ctx.send("Yo, api key gotta be set first with the 'leagueapi <key>' command")
        if ctx.channel.permissions_for(discord.utils.get(ctx.guild.members, id=ctx.bot.user.id)).add_reactions:
            return result
        else:
            raise commands.ReactionsCheckFailure(message="I got no permissions to add reactions")
    return commands.check(predicate)

class Leaguehell(commands.Cog):
    """The (__very unfinished__) Hell League Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.lib = Leaguelib(bot)
        self.handle = Handler(bot)
        default_global = {"leagueapikey": None}
        default_member = {
            "Name": None,
            "Region": "eune",
        }
        default_guild = {
            "db": []
        }
        self.config = Config.get_conf(self, identifier=690430666, force_registration=True)
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)
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

    async def user_lname(self, name: discord.Member=None):
        re = await self.config.member(name).Name()
        return re

    async def findshit(self, guild, authorname, search):
        #re = {"nick": "None", "region": "eune"}
        searchname = "None"
        ugherror = ">>> \nError \n"
        if type(search) is discord.Member:
            searchname = await self.config.member(search).Name()
            searchreg = await self.config.member(search).Region()
            return search, searchreg
        else:
            if str(search) == "None":
                searchauthor = await guild.get_member_named(authorname)
                searchname = await self.config.member(searchauthor).Name()
                searchreg = await self.config.member(searchauthor).Region()
                return search, searchreg
                if str(searchname) == "None":
                    err_regauthor = ">>> Whoa, {authorname.mention}, you haven't registered your league name. \nThat can be done with `!!league setname <name>`"
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
                searchauthor = await guild.get_member_named(authorname)
                searchname = await self.config.member(searchauthor).Name()
                searchreg = await self.config.member(searchauthor).Region()
                return search, searchreg
        if str(searchname) == "None":
            err_horseshit = ">>> Well horseshit, that person hasn't set their league name."
            return ugherror, err_horseshit
        else:
            return search, searchreg

    async def findshit_member(self, search):
        searchname = await self.config.member(search).Name()
        searchreg = await self.config.member(search).Region()
        if searchname == "None":
            return "Error", "Error"
        else:
            return searchname, searchreg

    async def findshit_string(self, search):
        if str(search) != "None":
            if len(search.split()) > 1:
                searchlast = search.split()[-1]
                searchlastl = searchlast.lower()
                searchlastc = searchlast.upper()
                if searchlastc in self.regchecks:
                    searchreg = self.servers[searchlastl]
                    searchcut = search.rsplit(" ", 1)[0]
                    searchname = searchcut
                    return searchname, searchreg
                else:
                    searchname = search
                    searchreg = self.servers["eune"]
                    return searchname, searchreg

    @checks.is_owner()
    @commands.command(name="leagueapi")
    async def leagueapi(self, ctx, *, key):
        """Set a key to use the league api"""
        await self.bot.db.api_tokens.set_raw("leaguehell", value={'leagueapikey': key})
        await ctx.send("gg wp")

    # League group
    @commands.group(name="league", no_pm=True)
    async def league(self, ctx):
        """Check / update the things in your profile"""
        pass

    # Drophere db gg
    @checks.is_owner()
    @league.command(pass_context=True, no_pm=True)
    async def drophere(self, ctx):
        server = ctx.guild
        db = await self.config.guild(server).db()
        #await ctx.send(box(text=db, lang="py"))
        asyncio.sleep(1)
        #ugh = await self.config.member().Name
        tlist = []
        temp = 0
        for i in db:
            #lookupuser = discord.utils.get(ctx.guild.members, id=i)
            lookupuser = self.bot.get_user(i)
            #lookupnick = await self.config.member(lookupuser[])
            #await ctx.send(box(text=i, lang="py"))
            if lookupuser:
                tlist.append(lookupuser)
            else:
                pass
            asyncio.sleep(1)
            temp += 1
            if temp >= 10:
                break
        asyncio.sleep(1)
        await ctx.send(box(text=tlist, lang="py"))

    @league.command(pass_context=True, no_pm=True)
    async def name(self, ctx, user: discord.Member=None):
        author = ctx.author
        if not user:
            user = ctx.author
        if user.is_avatar_animated():
            av = user.avatar_url_as(format="gif")
        else:
            av = user.avatar_url_as(format="png")
        aname = await self.config.member(user).Name()
        em = discord.Embed(colour=15158332)
        em.set_thumbnail(url=av)
        emdesc = (f"**{user}**'s summoner name:")
        em.description = emdesc
        em.add_field(name=u'\u200b', value=u'\u200b'f"**{aname}**")
        em.set_footer(text=(f"Powered by HELL | Requested by {author} | {vversion}"))
        await ctx.send(embed=em)

    @league.command(pass_context=True, no_pm=True)
    async def setname(self, ctx, name, user: discord.Member=None):
        """Set your league nickname. \nIf it has spaces put it in quotes ("Two words").\n\n`[user]` is an optional parameter for Moderators to set other people's nicknames."""
        server = ctx.guild
        author = ctx.author
        tar = None
        checkmod = await self.handle.check_modadmin(author)
        if not user:
            tar = author
        else:
            if checkmod is True:
                tar = user
            else:
                if user == author:
                    tar = author
                else:
                    await ctx.send("> You can't set other people's nicknames")
                    return
        #await ctx.send(f"> __**DEBUG**__ \nTar is set to {tar}\nCaller is {author}\nCheck is {checkmod}\nVar is set to {name}")
        #try:
        db = await self.config.guild(server).db()
        if tar.id in db:
            await self.config.member(tar).Name.set(name)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name=f"**{tar}**'s nickname has been changed to **{name}**", value=f"Issued by {author}")
            data.set_footer(text=f"Powered by HELL | {vversion}")
            await ctx.send(embed=data)
        else:
            db.append(tar.id)
            await self.config.guild(server).db.set(db)
            await self.config.member(tar).Name.set(name)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name=f"**{tar}**'s nickname has been changed to **{name}**", value=f"Issued by {author}")
            data.set_footer(text=f"Powered by HELL | {vversion}")
            await ctx.send(embed=data)
        #except:
        #    await ctx.send("Welp, that didn't work out. I think.")

    @league.command(pass_context=True, no_pm=True, name="setreg", aliases=["setregion"])
    async def setreg(self, ctx, reg: str, user: discord.Member=None):
        """Set your league region. \n\n`[user]` is an optional parameter for Moderators to set other people's regions."""
        server = ctx.guild
        author = ctx.author
        tar = None
        regchecks = ["EUNE", "EUW", "NA"]
        checkmod = await self.handle.check_modadmin(author)
        if not user:
            tar = author
        else:
            if checkmod is True:
                tar = user
            else:
                if user == author:
                    tar = author
                else:
                    await ctx.send("> You can't set other people's region")
                    return
        db = await self.config.guild(server).db()
        if reg.upper() in regchecks:
            if tar.id in db:
                regup = reg.upper()
                reglow = reg.lower()
                await self.config.member(tar).Region.set(reglow)
                data = discord.Embed(colour=0xff0000)
                data.add_field(name=f"**{tar}**'s region has been changed to **{regup}**", value=f"Issued by {author}")
                data.set_footer(text=f"Powered by HELL | {vversion}")
                await ctx.send(embed=data)
            else:
                regup = reg.upper()
                reglow = reg.lower()
                db.append(tar.id)
                await self.config.guild(server).db.set(db)
                await self.config.member(tar).Region.set(reglow)
                data = discord.Embed(colour=0xff0000)
                data.add_field(name=f"**{tar}**'s nickname has been changed to **{regup}**", value=f"Issued by {author}")
                data.set_footer(text=f"Powered by HELL | {vversion}")
                await ctx.send(embed=data)
        else:
            regup = reg.upper()
            reglow = reg.lower()
            data = discord.Embed(colour=0xff0000)
            data.add_field(name=f"**{regup}** is not a valid region.", value=f"Valid regions are: \n{regchecks}")
            data.set_footer(text=f"Powered by HELL | {vversion}")
            await ctx.send(embed=data)


    @checks.is_owner()
    @commands.command(name="leakapi")
    async def leakapi(self, ctx):
        """Leaks your api key. Gj."""
        db = await self.bot.db.api_tokens.get_raw("leaguehell", default=None)
        await ctx.send(db["leagueapikey"])
    
    # One embed
    #@checks.is_owner()
    @league.command(name="champs", aliases=["champions"])
    @apikeycheck()
    async def champs(self, ctx, name: Union[discord.Member, str] = None, xreg=None):
        author = ctx.author
        if not xreg:
            if not self.config.member(author).Region():
                await ctx.send_help()
                return
            else:
                xreg = await self.config.member(author).Region()
        if not name:
            if not self.config.member(author).Name():
                await ctx.send_help()
                return
            else:
                name = await self.config.member(author).Name()
        if type(name) is discord.Member:
            reg = await self.user_lname(name)
            if reg == "None":
                return "> No account set"
            else:
                name = reg
        #dnname = usr.display_name
        sumname = str(name).capitalize()
        summname = await self.lib.get_prname(name, xreg)
        if summname == "None":
            await ctx.send("> This user has no account set :(")
            return
        em = discord.Embed(colour=15158332)
        icostr = str(await self.lib.summ_icon(name, xreg))
        total = await self.lib.get_mastery(name, xreg)
        emdesc = (f"**{sumname}**\nTotal mastery: **{total}**\n**Top 3 champions by mastery**:")
        em.description = emdesc
        em.url = icostr
        em.set_footer(text=(f"Powered by HELL | Requested by {author} | {vversion}"), icon_url=icostr)
        champs = await self.lib.get_champ_masteries(name, xreg)
        temp = 0
        for i in champs:
            chname = await self.lib.get_champ_name(str(i["championId"]))
            chnames = await self.lib.champ_name_sanitized(str(i["championId"]))
            chemoji = await self.lib.champ_emoji(chnames)
            clvl = i["championLevel"]
            cpoints = i["championPoints"]
            cchest = i["chestGranted"]
            if cchest is True:
                chest = "Yes"
            else:
                chest = "No"
            cmtokens = i["tokensEarned"]
            cmlpunix = (i["lastPlayTime"]/1000)
            cmlp = datetime.datetime.fromtimestamp(cmlpunix).strftime('%Y-%m-%d')
            em.add_field(name=(f"{chemoji} {chname}"), value=(f"At **{cpoints}** points.\nLevel **{clvl}**.\n**{cmtokens}** tokens.\nChest granted? **{chest}**.\nLast played: **{cmlp}**."), inline=True)
            temp += 1
            if temp >= 3:
                break
            await asyncio.sleep(0.5)
        await ctx.send(embed=em)
        # End of one embed

    # Paginated mastery
    #@checks.is_owner()
    @league.command(name="pchamps", aliases=["pchampions"])
    @apikeycheck()
    async def pchamps(self, ctx, name: Union[discord.Member, str] = None, xreg=None):
        author = ctx.author
        if not xreg:
            if not self.config.member(author).Region():
                await ctx.send_help()
                return
            else:
                xreg = await self.config.member(author).Region()
        if not name:
            if not self.config.member(author).Name():
                await ctx.send_help()
                return
            else:
                name = await self.config.member(author).Name()
        if type(name) is discord.Member:
            reg = await self.user_lname(name)
            if reg == "None":
                return "> No account set"
            else:
                name = reg
        sumname = await self.lib.get_prname(name, xreg)
        if sumname == "None":
            await ctx.send("> This user has no account set :(")
            return
        icostr = str(await self.lib.summ_icon(name, xreg))
        clist = []
        #dnname = usr.display_name
        total = await self.lib.get_mastery(name, xreg)
        champs = await self.lib.get_champ_masteries(name, xreg)
        cpage = 0
        #tpages = 10
        for i in champs:
            cpage += 1
            if cpage >= 11:
                break
            em = discord.Embed(colour=15158332)
            chname = await self.lib.get_champ_name(str(i["championId"]))
            chtitle = await self.lib.get_champ_title(str(i["championId"]))
            chico = str(await self.lib.ddragon_champico(str(i["championId"])))
            csplash = str(await self.lib.ddragon_champsplash(str(i["championId"])))
            clvl = i["championLevel"]
            cpoints = i["championPoints"]
            cchest = i["chestGranted"]
            if cchest is True:
                chest = "Yes"
            else:
                chest = "No"
            cmtokens = i["tokensEarned"]
            cmlpunix = (i["lastPlayTime"]/1000)
            cmlp = datetime.datetime.fromtimestamp(cmlpunix).strftime('%Y-%m-%d')
            emdesc = f"**{cpoints}** points."
            em.set_footer(text=(f"Page {cpage}/10 | Total mastery: {total} | Powered by HELL | Requested by {author} | {vversion}"), icon_url=icostr)
            em.description = emdesc
            clist.append(em)
            em.set_author(name=f"{chname}, {chtitle}", url=f"{chico}", icon_url=f"{chico}")
            em.add_field(name=f"Level **{clvl}**", value=f"**{cmtokens}** tokens.", inline=True)
            em.add_field(name="Chest granted?", value=f"**{chest}**", inline=True)
            em.add_field(name="Last played:", value=f"**{cmlp}**", inline=True)
            em.add_field(name="Default splash art", value=f"[Click here to view]({csplash})", inline=True)
            em.set_image(url=csplash)
            await asyncio.sleep(0.3)
        await menu(ctx, pages=clist, timeout=30, controls=DEFAULT_CONTROLS)


    @checks.is_owner()
    @league.command(name="rankedold")
    async def rankedold(self, ctx, name=None, xreg=None):
        """/gonna set help when I can/"""
        author = ctx.author
        if not xreg:
            if not self.config.member(author).Region():
                await ctx.send_help()
                return
            else:
                xreg = await self.config.member(author).Region()
        if not name:
            if not self.config.member(author).Name():
                await ctx.send_help()
                return
            else:
                name = await self.config.member(author).Name()
        if "#" in name: 
            reg = await self.handle.search_leaguename(name)
            if reg == "Error":
                return "> No account set"
            else:
                name = reg
            #return xreg
        icostr = str(await self.lib.summ_icon(name, xreg))
        uhelo = await self.lib.get_ranked(name, xreg)
        try:
            opgg = f"https://{xreg}.op.gg/summoner/userName={name}"
        except:
            opgg = None
        propername = await self.lib.get_prname(name, xreg)
        em = discord.Embed(colour=15158332)
        if not opgg:
            em.set_author(name=f"{propername}", icon_url=f"{icostr}")
        else:
            em.set_author(name=f"{propername} (op.gg link)", url=f"https://{xreg}.op.gg/summoner/userName={name}", icon_url=f"{icostr}")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        xregc = xreg.upper()
        em.description = (f"{xregc} **{propername}** Ranked stats")
        picon = str(await self.lib.summ_icon(name, xreg))
        em.set_thumbnail(url=picon)
        #uhelo = await self.lib.ranked_q(uhelo)
        for i in uhelo:
            queuetype = i["queueType"]
            if queuetype == "Teamfight Tactics":
                em.add_field(name="**Note:**", value="*Winratio is not really realistic in TFT, as RIOT counts only 1st place for a win (2nd to 8th are all counted as losses).*", inline=False)
            wins = i["wins"]
            losses = i["losses"]
            tier = i["tier"]
            rank = i["rank"]
            leaguepnts = i["leaguePoints"]
            totalgames = int(wins)+int(losses)
            calcratio = (int(wins)/totalgames)*100
            ratio = round(calcratio, 2)
            em.add_field(name=(f"{queuetype}"), value=(f" :white_small_square: **{tier}** {rank} \n :white_small_square: **{leaguepnts}** LP \n :white_small_square: Wins/losses: **{wins}**/**{losses}** \n  :white_small_square: **{totalgames}** total games, **{ratio}%** winrate"), inline=False)
            await asyncio.sleep(0.5)
        await ctx.send(embed=em)
    
    #@checks.is_owner()
    @league.command(name="ranked")
    async def ranked(self, ctx, name: Union[discord.Member, str] = None, xreg=None):
        author = ctx.author
        if not xreg:
            if not self.config.member(author).Region():
                await ctx.send_help()
                return
            else:
                xreg = await self.config.member(author).Region()
        if not name:
            if not self.config.member(author).Name():
                await ctx.send_help()
                return
            else:
                name = await self.config.member(author).Name()
        if type(name) is discord.Member:
            reg = await self.user_lname(name)
            if reg == "None":
                return "> No account set"
            else:
                name = reg
        propername = await self.lib.get_prname(name, xreg)
        if propername == "None":
            await ctx.send("> This user has no account set :(")
            return
        uhelo = await self.lib.get_ranked(name, xreg)
        try:
            opgg = f"https://{xreg}.op.gg/summoner/userName={name}"
        except:
            opgg = None
        icostr = str(await self.lib.summ_icon(name, xreg))
        em = discord.Embed(colour=15158332)
        if not opgg:
            em.set_author(name=f"{propername}", icon_url=f"{icostr}")
        else:
            em.set_author(name=f"{propername} (op.gg link)", url=f"https://{xreg}.op.gg/summoner/userName={name}", icon_url=f"{icostr}")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        xregc = xreg.upper()
        em.description = (f"{xregc} **{propername}** Ranked stats")
        picon = str(await self.lib.summ_icon(name, xreg))
        em.set_thumbnail(url=picon)
        for i in uhelo:
            queuetype = i["queueType"]
            if queuetype == "Teamfight Tactics":
                em.add_field(name="**Note:**", value="*Winratio is not really realistic in TFT, as RIOT counts only 1st place for a win (2nd to 8th are all counted as losses).*", inline=False)
            wins = i["wins"]
            losses = i["losses"]
            tier = i["tier"]
            tiermoji = tier.lower()
            emoji = await self.lib.champ_emoji(str(tiermoji).capitalize())
            rank = i["rank"]
            leaguepnts = i["leaguePoints"]
            totalgames = int(wins)+int(losses)
            calcratio = (int(wins)/totalgames)*100
            ratio = round(calcratio, 2)
            em.add_field(name=(f"{queuetype}"), value=(f" {emoji} **{tier}** {rank} \n :white_small_square: **{leaguepnts}** LP \n :white_small_square: Wins/losses: **{wins}**/**{losses}** \n  :white_small_square: **{totalgames}** total games, **{ratio}%** winrate"), inline=False)
            await asyncio.sleep(0.5)
        await ctx.send(embed=em)

    @checks.is_owner()
    @commands.command(name="champlist")
    async def champlist(self, ctx):
        clist = []
        champid = await self.lib.get_champlist()
        npages = len(champid)
        cpage = 0
        for i in champid:
            cpage += 1
            thing1 = champid[i]["name"]
            thing2 = champid[i]["key"]
            thing3 = champid[i]["id"]
            thing4 = champid[i]["title"]
            thing5 = champid[i]["blurb"]
            em = discord.Embed(colour=15158332)
            emdesc = f"**{thing1}** / ID: {thing3}."
            em.add_field(name=f"Key: {thing2}, {thing4}", value=f"{thing5}")
            em.set_footer(text=(f"Page {cpage}/{npages} | Powered by HELL | {vversion}"))
            em.description = emdesc
            clist.append(em)
        await menu(ctx, pages=clist, timeout=30, controls=DEFAULT_CONTROLS)

    @checks.is_owner()
    @commands.command(name="champ")
    async def champ(self, ctx, *, name):
        author = ctx.author
        data = await self.lib.cdragon_champ_data(name)
        if data != "Error":
            chname = data["name"]
            chtitle = data["title"]
            chbio = data["shortBio"]
            chico = await self.lib.cdragon_champ_square(name)
            chpassivename = data["passive"]["name"]
            chpassivedescrx = data["passive"]["description"]
            chpassivedescr = await self.handle.cleanhtml(chpassivedescrx)
            chroles = data["roles"]
            em = discord.Embed(colour=15158332)
            em.set_author(name=f"{chname}, {chtitle}", url=f"{chico}", icon_url=f"{chico}")
            allroles = " ".join([str(elem) for elem in chroles])
            em.add_field(name="Roles:", value=f"{allroles}")
            emdesc = f"{chname}, {chtitle} \n{chbio}"
            em.add_field(name="Emoji test:", value=f"__/chemoji-placeholder/__", inline=False)
            em.add_field(name=f"Passive: **{chpassivename}**", value=f"{chpassivedescr}", inline=False)
            em.set_footer(text=f"Powered by HELL | Requested by {author} | ChampionID: \obsolete\ | {vversion}")
        else:
            em = discord.Embed(colour=15158332)
            emdesc = "**Invalid champ**"
            em.description = emdesc
            em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        await ctx.send(embed=em)

    @league.command(name="status")
    async def status(self, ctx, xreg=None):
        author = ctx.author
        if not xreg:
            if not self.config.member(author).Region():
                await ctx.send_help()
                return
            else:
                xreg = await self.config.member(author).Region()
        xreglow = xreg.lower()
        rq = await self.lib.statusdata(xreglow)
        if rq is False:
            await ctx.send("> This ain't a valid region what ze fuck")
            return
        region = rq["name"]
        hostname = rq["hostname"]
        srvcs = rq["services"]
        em = discord.Embed(colour=15158332)
        em.set_author(name=f"Server status for {region} at {hostname}")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        for i in srvcs:
            status = str(i["status"]).capitalize()
            emojistatus = status.lower()
            emoji = await self.lib.champ_emoji(emojistatus)
            incidents = i["incidents"]
            name = i["name"]
            if len(incidents) == 0:
                em.add_field(name=f"{emoji} {name}: {status}", value=f"No issues", inline=False)
            else:
                incident = []
                number = 0
                for i in incidents:
                    incid = i["id"]
                    active = i["active"]
                    created = i["created_at"]
                    updates = i["updates"]
                    if updates:
                        for u in updates:
                            updated = u["updated_at"]
                            content = u["content"]
                            severity = str(u["severity"]).capitalize()
                            ucreated = u["created_at"]
                            incident.append(f"`Incident ID:`\n{incid}\n`Active:`\n**{active}**\n`Created at:`\n{created}\n`Updated at:`\n{updated}\n`Category:`\n**{severity}**\n`Information:`\n{content}")
                report = "\n".join(incident)
                em.add_field(name=f"{emoji} {name}: {status}", value=f"**Incidents:**\n{report}", inline=False)
        await ctx.send(embed=em)
            
    @commands.command(name="leaguepatch")
    async def leaguepatch(self, ctx):
        cpatch = await self.lib.get_patch()
        await ctx.send(box(cpatch))

    @checks.is_owner()
    @league.command(name="champid")
    async def champid(self, ctx, *, champ: Union[str, int] = None):
        if type(name) is str:
            champinfo = await self.lib.get_champ
    
    @checks.is_owner()
    @league.command(name="listmastery")
    async def listmastery(self, ctx, name: Union[discord.Member, str] = None, xreg=None):
        author = ctx.author
        if not xreg:
            if not self.config.member(author).Region():
                await ctx.send_help()
                return
            else:
                xreg = await self.config.member(author).Region()
        if not name:
            if not self.config.member(author).Name():
                await ctx.send_help()
                return
            else:
                name = await self.config.member(author).Name()
        if type(name) is discord.Member:
            reg = await self.user_lname(name)
            if reg == "None":
                return "> No account set"
            else:
                name = reg
        clist = []
        total = await self.lib.get_mastery(name, xreg)
        icostr = str(await self.lib.summ_icon(name, xreg))
        champs = await self.lib.get_champ_masteries(name, xreg)
        cpage = 0
        for i in champs:
            cpage += 1
            if cpage >= 11:
                break
            em = discord.Embed(colour=15158332)
            chname = await self.lib.get_champ_name(str(i["championId"]))
            chtitle = await self.lib.get_champ_title(str(i["championId"]))
            clvl = i["championLevel"]
            cpoints = i["championPoints"]
            cchest = i["chestGranted"]
            if cchest is True:
                chest = "Yes"
            else:
                chest = "No"
            cmtokens = i["tokensEarned"]
            cmlpunix = (i["lastPlayTime"]/1000)
            cmlp = datetime.datetime.fromtimestamp(cmlpunix).strftime('%Y-%m-%d')
            emdesc = f"**{cpoints}** points."
            em.set_footer(text=(f"Page {cpage}/10 | Total mastery: {total} | Powered by HELL | Requested by {author} | {vversion}"), icon_url=icostr)
            em.description = emdesc
            clist.append(em)
            em.set_author(name=f"{chname}, {chtitle}")
            em.add_field(name=f"Level **{clvl}**", value=f"**{cmtokens}** tokens.", inline=True)
            em.add_field(name="Chest granted?", value=f"**{chest}**", inline=True)
            em.add_field(name="Last played:", value=f"**{cmlp}**", inline=True)
            await asyncio.sleep(0.3)
        await menu(ctx, pages=clist, timeout=30, controls=DEFAULT_CONTROLS)

    @checks.is_owner()
    @commands.command(name="leaguetestname")
    async def leaguetestname(self, ctx, name: discord.Member=None):
        test = await self.handle.get_leaguename(name)
        if test == "Error":
            await ctx.send("> Name not found or some shit")
        else:
            await ctx.send("> Name is in the DB")
    
    @checks.is_owner()
    @commands.command(name="leagueemoji")
    async def leagueemoji(self, ctx, *, name):
        chemoji = await self.lib.champ_emoji(name)
        await ctx.send(chemoji)

    @checks.is_owner()
    @commands.command(name="testelo")
    async def testelo(self, ctx, *, search: Union[discord.Member, str] = None):
        author = ctx.author
        #WIP
        

    #@checks.is_owner()
    @commands.command(name="testshit")
    async def testshit(self, ctx, *, search: Union[discord.Member, str] = None):
        author = ctx.author
        searchreg = "eun1"
        if str(search) is "None":
            searchname, searchreg = await self.findshit_member(author)
        elif type(search) is discord.Member:
            searchname, searchreg = await self.findshit_member(search)
        elif type(search) is str:
            searchname, searchreg = await self.findshit_string(search)
        await ctx.send(f"Search value: {searchname} \nSearchreg value: {searchreg}")
        await ctx.send("Done.")

    def cog_unload(self):
        self.lib.cog_unload()

    __del__ = cog_unload