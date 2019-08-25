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

vversion = "version: 0.05"
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
        self.regchecks = ["EUNE", "EUW", "NA"]

    async def user_lname(self, name: discord.Member=None):
        re = await self.config.member(name).Name()
        return re

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
        #await ctx.send(box(text=aname, lang="ruby"))

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
            #cload = str(await self.lib.ddragon_champsloading(str(i["championId"])))
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
            #em.set_thumbnail(url=cload)
            #emdesc = f"__**{chname}**__ \n\nAt **{cpoints}** points."
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
        #try:
        #    not_mumbojumbo_anymore_biatch = other_dict[this_dict["queueType"]]
        #except KeyError:
        #    await ctx.send("ABORT MISSION! I REPEAT! ABORT MISSION!")
        #    return
        author = ctx.author
        #guild = ctx.guild
        if not xreg:
            if not self.config.member(author).Region():
                await ctx.send_help()
                return
            else:
                xreg = await self.config.member(author).Region()
        #if name is discord.Member:
        #    if not self.config.member(author).Name():
        #        await ctx.send_help()
        #    else:
        #        name = await self.config.member(name).Name()
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
        #author = ctx.author
        #allmembers = await self.config.all_members()
        #resp = ["> So:\n"]
        #if name is None:
        #    tar = await self.config.member(author).Name()
        #    resp.append(f"> No name, get author's from conf ({tar})")
        #else:
        #    try:
        #        tar = await self.config.member(user).Name()
        #        resp.append(f"> Name is in allmembers, get it from conf ({tar})")
        #    except:
        #        tar = name
        #        resp.append(f"> User ain't in allmembers and isn't the author, target is {tar}")
        #if not xreg:
        #    xreg = "eune"
        #    resp.append(f"> No xreg, defaults ({xreg})")
        #for i in resp:
        #    await ctx.send(i)
        #    asyncio.sleep(0.2)
        #
        #
        #champico = await self.lib.cdragon_champ_square(name)
        #await ctx.send(file=discord.File(champico, '{}.png'.format(name)))
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
        #guilds = [612586360473124865, 612586558528290837, 612586640413818881, 612586727726383104]
        #chkey = await self.lib.get_champid(name)
        #await ctx.send(chkey)
        data = await self.lib.cdragon_champ_data(name)
        if data != "Error":
            #list1 = ["Alistar", "Amumu", "Anivia", "Annie", "Ashe", "Blitzcrank", "Caitlyn", "ChoGath", "Corki", "DrMundo", "Evelynn", "Fiddlesticks", "Galio", "Gangplank", "Irelia", "Janna", "Jax", "Karma", "Karthus", "Kassadin", "Kayle", "LeBlanc", "MasterYi", "MissFortune", "Morgana", "None", "Nunu", "Olaf", "Rammus", "Ryze", "Shaco", "Singed", "Sion", "Sivir", "Sona", "Soraka", "Swain", "Taric", "Teemo", "Tristana", "Trundle", "Tryndamere", "TwistedFate", "Twitch", "Urgot", "Veigar", "Vladimir", "Warwick", "XinZhao", "Zilean"]
            #list2 = ["Ahri", "Akali", "Brand", "Cassiopeia", "Draven", "Elise", "Ezrael", "Fiora", "Fizz", "Garen", "Gragas", "Graves", "Heimerdinger", "JarvanIV", "Katarina", "Kennen", "KogMaw", "LeeSin", "Leona", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "Mordekaiser", "Nasus", "Nautilus", "Nidalee", "Nocturne", "Orianna", "Pantheon", "Poppy", "Renekton", "Rengar", "Riven", "Rumble", "Sejuani", "Shen", "Shyvana", "Skarner", "Talon", "Udyr", "Varus", "Vayne", "Viktor", "Volibear", "Wukong", "Xerath", "Yorick", "Ziggs"]
            #list3 = ["Aatrox", "AurelionSol", "Azir", "Bard", "Braum", "Camilee", "Darius", "Diana", "Ekko", "Gnar", "Hecarim", "Illaloi", "Ivern", "Jayce", "Jhin", "Jinx", "KaiSa", "Kalista", "Kayn", "KhaZix", "Kindred", "Kled", "Lissandra", "Lucian", "Nami", "Neeko", "Ornn", "Pyke", "Qiyana", "Quinn", "Rakan", "RekSai", "Sylas", "Syndra", "TahmKench", "Taliyah", "Thresh", "VelKoz", "Vi", "Xayah", "Yasuo", "Yummi", "Zac", "Zed", "Zoe", "Zyra"]
            #guid1 = 612586360473124865
            #guid2 = 612586558528290837
            #guid3 = 612586640413818881
            #chid = data["id"]
            #if chid in list1:
            #    guildid = guid1
            #if chid in list2:
            #    guildid = guid2
            #if chid in list3:
            #    guildid = guid3
            #chemoji = get(bot.get_all_emojis(), name="Annie")
            chname = data["name"]
            chtitle = data["title"]
            chbio = data["shortBio"]
            chico = await self.lib.cdragon_champ_square(name)
            chpassivename = data["passive"]["name"]
            chpassivedescrx = data["passive"]["description"]
            chpassivedescr = await self.handle.cleanhtml(chpassivedescrx)
            chroles = data["roles"]
            #chspells = data["spells"]
            em = discord.Embed(colour=15158332)
            em.set_author(name=f"{chname}, {chtitle}", url=f"{chico}", icon_url=f"{chico}")
            #listroles = []
            #roles = len(chroles)
            allroles = " ".join([str(elem) for elem in chroles])
            #    for i in listroles:
            #        allroles = ''.join(listroles[i])
            em.add_field(name="Roles:", value=f"{allroles}")
            #for i in range(4):
                #spell = chspells[i]
                #hotkey = str(spell["spellkey"]).upper()
                #spname = spell["name"]
            emdesc = f"{chname}, {chtitle} \n{chbio}"
            #emoji = discord.utils.get(guild.emojis, name=f"{chid}")
            em.add_field(name="Emoji test:", value=f"__/chemoji-placeholder/__", inline=False)
            em.add_field(name=f"Passive: **{chpassivename}**", value=f"{chpassivedescr}", inline=False)
            em.set_footer(text=f"Powered by HELL | Requested by {author} | ChampionID: \obsolete\ | {vversion}")
        else:
            em = discord.Embed(colour=15158332)
            emdesc = "**Invalid champ**"
            em.description = emdesc
            em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
        await ctx.send(embed=em)
        #await ctx.send(len(data["spells"]))

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
        #tpages = 10
        for i in champs:
            cpage += 1
            if cpage >= 11:
                break
            em = discord.Embed(colour=15158332)
            chname = await self.lib.get_champ_name(str(i["championId"]))
            chtitle = await self.lib.get_champ_title(str(i["championId"]))
            #chico = str(await self.lib.ddragon_champico(str(i["championId"])))
            #csplash = str(await self.lib.ddragon_champsplash(str(i["championId"])))
            #cload = str(await self.lib.ddragon_champsloading(str(i["championId"])))
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
            #em.set_thumbnail(url=cload)
            #emdesc = f"__**{chname}**__ \n\nAt **{cpoints}** points."
            emdesc = f"**{cpoints}** points."
            em.set_footer(text=(f"Page {cpage}/10 | Total mastery: {total} | Powered by HELL | Requested by {author} | {vversion}"), icon_url=icostr)
            em.description = emdesc
            clist.append(em)
            em.set_author(name=f"{chname}, {chtitle}")
            em.add_field(name=f"Level **{clvl}**", value=f"**{cmtokens}** tokens.", inline=True)
            em.add_field(name="Chest granted?", value=f"**{chest}**", inline=True)
            em.add_field(name="Last played:", value=f"**{cmlp}**", inline=True)
            #em.add_field(name="Default splash art", value=f"[Click here to view]({csplash})", inline=True)
            await asyncio.sleep(0.3)
        await menu(ctx, pages=clist, timeout=30, controls=DEFAULT_CONTROLS)

    @checks.is_owner()
    @commands.command(name="leaguetestname")
    async def leaguetestname(self, ctx, name: discord.Member=None):
        #if "#" in name:
        #    test = await self.handle.search_leaguename(name)
        #    await ctx.send(test)
        #else:
        #    await ctx.send("> # not found")
        test = await self.handle.search_leaguename(name)
        if test == "Error":
            await ctx.send("> Name not found or some shit")
        else:
            await ctx.send("> Name is in the DB")
    
    @checks.is_owner()
    @commands.command(name="leagueemoji")
    async def leagueemoji(self, ctx, *, name):
        chemoji = await self.lib.champ_emoji(name)
        await ctx.send(chemoji)

    #@checks.is_owner()
    #@league.command(name="history")
    #async def history(self, ctx, name, xreg):
    #    """I mean. If I'm reading the help on my own command..."""
    #    author = ctx.author
    #    if not xreg:
    #        xreg = "eune"
    #    #icostr = str(await self.lib.summ_icon(name, xreg))
    #    clist = []
    #    cpage = 0
    #    hstry = await self.lib.get_history(name, xreg)
    #    #propername = await self.lib.get_prname(name, xreg)
    #    #em = discord.Embed(colour=15158332)
    #    #em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
    #    #em.description = (f"**{propername}**'s shit:")
    #    for i in hstry:
    #        cpage += 1
    #        if cpage >= 11:
    #            break
    #        em = discord.Embed(colour=15158332)
    #        em.set_footer(text=f"Powered by HELL | Requested by {author} | {vversion}")
    #        champ = hstry[i]["champ"]
    #        try:
    #            role = hstry[i]["role"]
    #        except:
    #            role = "n/a (r)"
    #        try:
    #            lane = hstry[i]["lane"]
    #        except:
    #            lane = "n/a (l)"
    #        duration = hstry[i]["Duration"]
    #        gamemode = hstry[i]["Gamemode"]
    #        result = hstry[i]["result"]
    #        kda = hstry[i]["kda"]
    #        gold = hstry[i]["gold"]
    #        em.description = (f"**{gamemode}** | {duration} min")
    #        em.add_field(name=(f"{champ} | r: {role} / l: {lane}"), value=(f"**{result}**\n{kda} | {gold}"), inline=False)
    #        clist.append(em)
    #        await asyncio.sleep(0.5)
    #    await menu(ctx, pages=clist, timeout=30, controls=DEFAULT_CONTROLS)