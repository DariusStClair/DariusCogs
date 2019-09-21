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
from .datalib import Datalib

vversion = "version: 0.07c"
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
        self.data = Datalib(bot)
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
        self.servers = self.data.SERVERS
        self.opggservers = self.data.OPGGSERVERS
        self.gametypes = self.data.GAMETYPES
        self.gamemodes = self.data.GAMEMODES

    async def user_lname(self, name: discord.Member=None):
        re = await self.config.member(name).Name()
        return re

    async def findshit_member(self, search):
        searchname = await self.config.member(search).Name()
        searchreg = await self.config.member(search).Region()
        if searchname == "None":
            return "Error", "Error"
        else:
            return searchname, searchreg

    async def findshit_string(self, search):
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

    async def findshit_onestring(self, search):
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
        em = discord.Embed(colour=15158332)
        veigar = "https://66.media.tumblr.com/a06904a426c8400efb27d274dff48944/tumblr_on1g2lljht1tnb6cko2_250.gif"
        em.set_thumbnail(url=veigar)
        em.description = (f"*Working...*\n\n")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        message = await ctx.send(embed=em)
        aname = await self.config.member(user).Name()
        areg = await self.config.member(user).Region()
        if aname is None:
            veigarq = "https://66.media.tumblr.com/098fef7a648679a31f25e33362b2602c/tumblr_on1g2lljht1tnb6cko3_250.gif"
            em.set_thumbnail(url=veigarq)
            emdesc = (f"Welp, that user doesn't have an account set")
            em.description = emdesc
        else:
            propername = await self.lib.get_prname(aname, areg)
            icostr = str(await self.lib.summ_icon(aname, areg))
            em.set_thumbnail(url=icostr)
            emdesc = (f"**{user}**'s summoner name(s):")
            em.description = emdesc
            em.add_field(name=f'**{propername}** ({areg})', value=u'\u200b')
        await message.edit(embed=em)

    @league.command(pass_context=True, no_pm=True)
    async def setname(self, ctx, *, name):
        """Set your league nickname."""
        server = ctx.guild
        tar = ctx.author
        author = tar
        db = await self.config.guild(server).db()
        if "@" in name or "#" in name:
            data = discord.Embed(colour=0xff0000)
            data.add_field(name=f"Nah mate, you gotta do like:", value=f"**!!league setname <whatever nickname>** (without the brackets)\nDon't tag anyone.")
            data.set_footer(text=f"An attempt was made by {author} | Powered by HELL | {vversion}")
            await ctx.send(embed=data)
            return
        if tar.id in db:
            await self.config.member(tar).Name.set(name)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name=f"**{tar}**'s nickname has been changed to:", value=f"**{name}**")
            data.set_footer(text=f"Powered by HELL | {vversion}")
            await ctx.send(embed=data)
        else:
            db.append(tar.id)
            await self.config.guild(server).db.set(db)
            await self.config.member(tar).Name.set(name)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name=f"**{tar}**'s nickname has been changed to:", value=f"**{name}**")
            data.set_footer(text=f"Powered by HELL | {vversion}")
            await ctx.send(embed=data)

    @league.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def modname(self, ctx, user: discord.Member = None, *, name):
        """Set someone else's league nickname."""
        server = ctx.guild
        author = ctx.author
        if user is None:
            data = discord.Embed(colour=0xff0000)
            data.add_field(name=f"Nah mate, you gotta do like:", value=f"**!!league modname @someone <whatever nickname>** (without the brackets)")
            data.set_footer(text=f"An attempt was made by {author} | Powered by HELL | {vversion}")
            await ctx.send(embed=data)
            return
        db = await self.config.guild(server).db()
        if user.id in db:
            await self.config.member(user).Name.set(name)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name=f"**{user}**'s nickname has been changed to:", value=f"**{name}**")
            data.set_footer(text=f"Change issued by {author} | Powered by HELL | {vversion}")
            await ctx.send(embed=data)
        else:
            db.append(user.id)
            await self.config.guild(server).db.set(db)
            await self.config.member(user).Name.set(name)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name=f"**{user}**'s nickname has been changed to:", value=f"**{name}**")
            data.set_footer(text=f"Change issued by {author} | Powered by HELL | {vversion}")
            await ctx.send(embed=data)

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
    async def champs(self, ctx, search: Union[discord.Member, str] = None):
        author = ctx.author
        searchreg = "eune"
        if not search:
            searchname, searchreg = await self.findshit_member(author)
        elif type(search) is discord.Member:
            searchname, searchreg = await self.findshit_member(search)
        elif type(search) is str:
            if len(search.split()) > 1:
                searchname, searchreg = await self.findshit_string(search)
            else:
                searchname, searchreg = await self.findshit_onestring(search)
        #dnname = usr.display_name
        sumname = str(searchname).capitalize()
        summname = await self.lib.get_prname(searchname, searchreg)
        if summname == "None":
            await ctx.send("> This user has no account set :(")
            return
        em = discord.Embed(colour=15158332)
        veigar = "https://66.media.tumblr.com/a06904a426c8400efb27d274dff48944/tumblr_on1g2lljht1tnb6cko2_250.gif"
        em.set_thumbnail(url=veigar)
        em.description = (f"*Working...*\n\nLooking for: \n**{searchname}**\nLooking up in: \n**{searchreg}**")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        message = await ctx.send(embed=em)
        em = discord.Embed(colour=15158332)
        icostr = str(await self.lib.summ_icon(searchname, searchreg))
        total = await self.lib.get_mastery(searchname, searchreg)
        emdesc = (f"**{sumname}**\nTotal mastery: **{total}**\n**Top 3 champions by mastery**:")
        em.description = emdesc
        em.url = icostr
        em.set_footer(text=(f"Powered by HELL | Requested by {author} | {vversion}"), icon_url=icostr)
        champs = await self.lib.get_champ_masteries(searchname, searchreg)
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
        await message.edit(embed=em)
        # End of one embed

    # Paginated mastery
    #@checks.is_owner()
    @league.command(name="pchamps", aliases=["pchampions"])
    @apikeycheck()
    async def pchamps(self, ctx, search: Union[discord.Member, str] = None):
        author = ctx.author
        searchreg = "eune"
        if not search:
            searchname, searchreg = await self.findshit_member(author)
        elif type(search) is discord.Member:
            searchname, searchreg = await self.findshit_member(search)
        elif type(search) is str:
            if len(search.split()) > 1:
                searchname, searchreg = await self.findshit_string(search)
            else:
                searchname, searchreg = await self.findshit_onestring(search)
        sumname = await self.lib.get_prname(searchname, searchreg)
        if sumname == "None":
            await ctx.send("> This user has no account set :(")
            return
        icostr = str(await self.lib.summ_icon(searchname, searchreg))
        clist = []
        #dnname = usr.display_name
        total = await self.lib.get_mastery(searchname, searchreg)
        champs = await self.lib.get_champ_masteries(searchname, searchreg)
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
        em = discord.Embed(colour=15158332)
        veigar = "https://66.media.tumblr.com/a06904a426c8400efb27d274dff48944/tumblr_on1g2lljht1tnb6cko2_250.gif"
        em.set_thumbnail(url=veigar)
        em.description = (f"*Working...*\n\nLooking for: \n**{searchname}**\nLooking up in: \n**{searchreg}**")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        message = await ctx.send(embed=em)
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
        await message.edit(embed=em)

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
        
    @checks.is_owner()
    @league.command(name="now")
    async def now(self, ctx, *, search: Union[discord.Member, str] = None):
        author = ctx.author
        searchreg = "eune"
        if not search:
            searchname, searchreg = await self.findshit_member(author)
        elif type(search) is discord.Member:
            searchname, searchreg = await self.findshit_member(search)
        elif type(search) is str:
            if " " in search:
                searchname, searchreg = await self.findshit_string(search)
            else:
                searchname, searchreg = await self.findshit_onestring(search)
        em = discord.Embed(colour=15158332)
        veigar = "https://66.media.tumblr.com/a06904a426c8400efb27d274dff48944/tumblr_on1g2lljht1tnb6cko2_250.gif"
        em.set_thumbnail(url=veigar)
        em.description = (f"*Working...*\n\nLooking for: \n**{searchname}**\nLooking up in: \n**{searchreg}**")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        message = await ctx.send(embed=em)
        res = await self.lib.game_info(searchname, searchreg)
        em.description = (f"{res}")
        await message.edit(embed=em)

    #@checks.is_owner()
    @commands.command(name="testshit")
    async def testshit(self, ctx, *, search: Union[discord.Member, str] = None):
        author = ctx.author
        searchreg = "eune"
        if not search:
            searchname, searchreg = await self.findshit_member(author)
        elif type(search) is discord.Member:
            searchname, searchreg = await self.findshit_member(search)
        elif type(search) is str:
            searchname, searchreg = await self.findshit_string(search)
        await ctx.send(f"Search value: {searchname} \nSearchreg value: {searchreg}")
        await ctx.send("Done.")

    @league.command(name="versions")
    async def versions(self, ctx):
        author = ctx.author
        cogver = vversion
        ddragonver = await self.lib.get_patch()
        await ctx.send(f">>> Current Leaguehell version: **{cogver}**\nCurrent CDN version: **{ddragonver}**")

    @commands.command(name="freerotation")
    async def freerotation(self, ctx):
        author = ctx.author
        em = discord.Embed(colour=15158332)
        veigar = "https://66.media.tumblr.com/a06904a426c8400efb27d274dff48944/tumblr_on1g2lljht1tnb6cko2_250.gif"
        em.set_thumbnail(url=veigar)
        em.description = (f"*Working...")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        message = await ctx.send(embed=em)
        searchreg = await self.config.member(author).Region()
        rall = await self.lib.champ_rotation(searchreg)
        clist = ["Shrug"]
        elist = []
        for shit, stuff in rall.items():
            #if stuff != "maxNewPlayerLevel":
            #    tempchamp = await self.lib.champ_name_sanitized(stuff)
            #    tempmoji = await self.lib.champ_emoji(tempchamp)
            #    elist.append(tempmoji)
            #    em.add_field(name=f"{shit}", value=f"{elist}")
            #else:
            #    em.add_field(name=f"Max new player level:", value=f"{stuff}")
            if shit != "maxNewPlayerLevel":
                if shit != "freeChampionIdsForNewPlayers":
                    length = len(stuff)
                    for i in range(length):
                        champid = int(stuff[i])
                        champname = await self.lib.get_champ_title(champid)
                        tempchamp = await self.lib.champ_name_sanitized(champid)
                        tempmoji = await self.lib.champ_emoji(tempchamp)
                        tempchampname = await self.lib.get_champ_name(champid)
                        spacemoji = await self.lib.champ_emoji("space")
                        asyncio.sleep(0.5)
                        champ = tempmoji + spacemoji
                        elist.append(champname)
                    em.add_field(name=f"{shit}", value=f"{elist}", inline=False)
        maikati = rall.items()
        em.description = (f"Max new player level is **10**.\n{maikati}")
        #row = 0
        #for i in freeids:
        #    champid = freeids[row]
        #    row += 1
        #    em.add_field(name=f"Champ id: {champid}", value=f"Stuff will go in here", inline=False)
        await message.edit(embed=em)

    @league.command(name="ranked")
    async def ranked(self, ctx, *, search: Union[discord.Member, str] = None):
        author = ctx.author
        searchreg = "eune"
        if not search:
            searchname, searchreg = await self.findshit_member(author)
        elif type(search) is discord.Member:
            searchname, searchreg = await self.findshit_member(search)
        elif type(search) is str:
            #if len(search.split()) > 1:
            #    searchname, searchreg = await self.findshit_string(search)
            #else:
            #    searchname, searchreg = await self.findshit_onestring(search)
            if " " in search:
                searchname, searchreg = await self.findshit_string(search)
            else:
                searchname, searchreg = await self.findshit_onestring(search)
        em = discord.Embed(colour=15158332)
        veigar = "https://66.media.tumblr.com/a06904a426c8400efb27d274dff48944/tumblr_on1g2lljht1tnb6cko2_250.gif"
        em.set_thumbnail(url=veigar)
        em.description = (f"*Working...*\n\nLooking for: \n**{searchname}**\nLooking up in: \n**{searchreg}**")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        message = await ctx.send(embed=em)
        try:
            propername = await self.lib.get_prname(searchname, searchreg)
        except:
            await ctx.send("> Can't find that summoner or some shit")
            return
        if propername == "None":
            await ctx.send("> This user has no account set :(")
            return
        uhelo = await self.lib.get_ranked(searchname, searchreg)
        searchreggg = self.opggservers[searchreg]
        if " " in searchname:
            searchnamegg = searchname.replace(" ", "+")
            opgg = f"https://{searchreggg}.op.gg/summoner/userName={searchnamegg}"
        else:
            opgg = f"https://{searchreggg}.op.gg/summoner/userName={searchname}"
        icostr = str(await self.lib.summ_icon(searchname, searchreg))
        icostr20 = icostr.replace(" ", "%20")
        if not opgg:
            em.set_author(name=f"{propername}", icon_url=f"{icostr20}")
        else:
            em.set_author(name=f"{propername} (op.gg link)", url=f"{opgg}", icon_url=f"{icostr20}")
        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        xreggg = self.opggservers[searchreg]
        xregc = xreggg.upper()
        em.description = (f"{xregc} **{propername}** Ranked stats")
        picon = str(await self.lib.summ_icon(searchname, searchreg))
        picon20 = picon.replace(" ", "%20")
        em.set_thumbnail(url=picon20)
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
        await message.edit(embed=em)

    def cog_unload(self):
        self.lib.cog_unload()

    __del__ = cog_unload