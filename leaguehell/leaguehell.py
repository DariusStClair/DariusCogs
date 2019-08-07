# Ugh I gotta start using notes and shit
import discord
# Red stuffs
from redbot.core import checks, Config, bank, commands
from redbot.core.utils import mod
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
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
        try:
            result = True if key["leagueapikey"] else False
        except:
            result = False
        if not result and ctx.invoked_with in dir(ctx.bot.get_cog("Leaguehell")):
            await ctx.send("Yo, api key gotta be set first with the 'leagueapi <key>' command")
        return result
    return commands.check(predicate)

class Leaguehell(commands.Cog):
    """The (__very unfinished__) Hell League Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.lib = Leaguelib(bot)
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

    async def check_modadmin(self, author: discord.Member):
        guild = author.guild
        if author == guild.owner:
            return True
        if await self.bot.is_owner(author):
            return True
        if await self.bot.is_admin(author):
            return True
        if await self.bot.is_mod(author):
            return True
        return False

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
        if not user:
            user = ctx.author
        aname = await self.config.member(user).Name()
        await ctx.send(box(text=aname, lang="ruby"))

    #######################
    # League Name subgroup
    #######################
    #@league.group()
    #async def name(self, ctx, user: discord.Member=None):
    #    author = ctx.author
    #    if not user:
    #        tar = author
    #    
    # 

    @league.command(pass_context=True, no_pm=True)
    async def setname(self, ctx, name, user: discord.Member=None):
        """Set your league nickname"""
        server = ctx.guild
        author = ctx.author
        tar = None
        checkmod = await self.check_modadmin(author)
        if not user:
            tar = author
        else:
            if checkmod is True:
                tar = user
            else:
                if user == author:
                    tar = author
                else:
                    await ctx.send("You can't set other people's nicknames")
        #await ctx.send(f"> __**DEBUG**__ \nTar is set to {tar}\nCaller is {author}\nCheck is {checkmod}\nVar is set to {name}")
        try:
            db = await self.config.guild(server).db()
            if tar.id in db:
                await self.config.member(tar).Name.set(name)
                data = discord.Embed(colour=0xff0000)
                data.add_field(name=f"**{tar}**'s nickname has been changed to **{name}**", value=f"Issued by {author}")
                await ctx.send(embed=data)
            else:
                db.append(tar.id)
                await self.config.guild(server).db.set(db)
                await self.config.member(tar).Name.set(name)
                data = discord.Embed(colour=0xff0000)
                data.add_field(name=f"**{tar}**'s nickname has been changed to **{name}**", value=f"Issued by {anick}")
                await ctx.send(embed=data)
        except:
            pass

    @checks.is_owner()
    @commands.command(name="leakapi")
    async def leakapi(self, ctx):
        """Leaks your api key. Gj."""
        db = await self.bot.db.api_tokens.get_raw("leaguehell", default=None)
        await ctx.send(db["leagueapikey"])
    
    # One embed
    @checks.is_owner()
    @league.command(name="champs", aliases=["champions"])
    @apikeycheck()
    async def champs(self, ctx, name, *, xreg=None):
        usr = ctx.author
        if not xreg:
            xreg = "eune"
            return xreg
        dnname = usr.display_name
        sumname = str(name).capitalize()
        em = discord.Embed(colour=15158332)
        icostr = str(await self.lib.summ_icon(name, xreg))
        emdesc = (f"{sumname}'s top 6 champions by mastery in {xreg}:")
        em.description = emdesc
        em.url = icostr
        total = await self.lib.get_mastery(name, xreg)
        em.set_footer(text=(f"{sumname} Total mastery: {total} | Requested by {dnname} | Powered by HELL"), icon_url=icostr)
        champs = await self.lib.get_champ_masteries(name, xreg)
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
            cmtokens = i["tokensEarned"]
            cmlpunix = (i["lastPlayTime"]/1000)
            cmlp = datetime.datetime.fromtimestamp(cmlpunix).strftime('%Y-%m-%d')
            em.add_field(name=(f"{chname}"), value=(f"At **{cpoints}** points.\nLevel **{clvl}**.\n**{cmtokens}** tokens.\nChest granted? **{chest}**.\nLast played: **{cmlp}**."), inline=True)
            if temp >= 8:
                break
            temp += 1
            await asyncio.sleep(0.5)
        await ctx.send(embed=em)
        # End of one embed

    # Paginated mastery
    #@checks.is_owner()
    @league.command(name="pchamps", aliases=["pchampions"])
    @apikeycheck()
    async def pchamps(self, ctx, name, *, xreg=None):
        usr = ctx.author
        if not xreg:
            xreg = "eune"
            return xreg
        icostr = str(await self.lib.summ_icon(name, xreg))
        clist = []
        dnname = usr.display_name
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
            chico = str(await self.lib.ddragon_champico(str(i["championId"])))
            csplash = str(await self.lib.ddragon_champsplash(str(i["championId"])))
            cload = str(await self.lib.ddragon_champsloading(str(i["championId"])))
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
            em.set_thumbnail(url=cload)
            #emdesc = f"__**{chname}**__ \n\nAt **{cpoints}** points."
            emdesc = f"**{cpoints}** points."
            em.set_footer(text=(f"Page {cpage}/10 | Total mastery: {total} | Requested by {dnname} | Powered by HELL"), icon_url=icostr)
            em.description = emdesc
            clist.append(em)
            em.set_author(name=f"{chname}", url=f"{chico}", icon_url=f"{chico}")
            em.add_field(name=f"Level **{clvl}**", value=f"**{cmtokens}** tokens.", inline=True)
            em.add_field(name="Chest granted?", value=f"**{chest}**", inline=True)
            em.add_field(name="Last played:", value=f"**{cmlp}**", inline=True)
            em.add_field(name="Default splash art", value=f"[Click here to view]({csplash})", inline=True)
            em.set_image(url=csplash)
            await asyncio.sleep(0.3)
        await menu(ctx, pages=clist, timeout=30, controls=DEFAULT_CONTROLS)


    @checks.is_owner()
    @league.command(name="lhtest")
    async def ranked(self, ctx, name, xreg):
        """... I'm doing something wrong"""
        #try:
        #    not_mumbojumbo_anymore_biatch = other_dict[this_dict["queueType"]]
        #except KeyError:
        #    await ctx.send("ABORT MISSION! I REPEAT! ABORT MISSION!")
        #    return
        author = ctx.author
        if xreg.lower() == "none":
            xreg = "eun1"
            return xreg
        uhelo = await self.lib.get_ranked(name, xreg)
        propername = await self.lib.get_prname(name, xreg)
        em = discord.Embed(colour=15158332)
        em.set_footer(text=f"Powered by HELL | Requested by {author} | version: 0.00")
        xregc = xreg.upper()
        em.description = (f"{xregc} **{propername}** Ranked stats")
        picon = str(await self.lib.summ_icon(name, xreg))
        em.set_thumbnail(url=picon)
        #uhelo = await self.lib.ranked_q(uhelo)
        for i in uhelo:
            queuetype = i["queueType"]
            wins = i["wins"]
            losses = i["losses"]
            tier = i["tier"]
            rank = i["rank"]
            leaguepnts = i["leaguePoints"]
            em.add_field(name=(f"{queuetype}"), value=(f"**{tier}** {rank} :white_small_square: **{leaguepnts}** LP :white_small_square: Wins/losses: **{wins}**/**{losses}**"), inline=False)
            await asyncio.sleep(0.5)
        await ctx.send(embed=em)

    @checks.is_owner()
    @commands.command(name="gettests")
    async def gettests(self, ctx, name, xreg):
        wtfwe = await self.lib.get_champ_masteries(name, xreg)
        await ctx.send(wtfwe)
    
    @checks.is_owner()
    @league.command(name="lhistory")
    async def history(self, ctx, name, xreg):
        """I mean. If I'm reading the help on my own command..."""
        author = ctx.author
        if xreg.lower() == "none":
            xreg = "eun1"
            return xreg
        hstry = await self.lib.get_history(name, xreg)
        propername = await self.lib.get_prname(name, xreg)
        em = discord.Embed(colour=15158332)
        em.set_footer(text=f"Powered by HELL | Requested by {author} | version: 0.00")
        em.description = (f"**{propername}**'s shit:")
        for i in hstry:
            champ = hstry[i]["champ"]
            role = hstry[i]["role"]
            duration = hstry[i]["Duration"]
            gamemode = hstry[i]["Gamemode"]
            result = hstry[i]["result"]
            kda = hstry[i]["kda"]
            gold = hstry[i]["gold"]
            em.add_field(name=(f"{gamemode} | {duration} minutes"), value=(f"**{champ}** | {role} | {result} | {kda} | {gold}"), inline=False)
            await asyncio.sleep(0.5)
        await ctx.send(embed=em)