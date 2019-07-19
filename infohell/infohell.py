# Ugh I gotta start using notes and shit
import discord
# Red stuffs
from redbot.core import checks, Config, bank, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils import mod
from redbot.core.utils.chat_formatting import bold, box, inline
import asyncio
import datetime
import random

class Infohell(commands.Cog):
    """The info Cog for Hell"""

    def __init__(self, bot):
        self.bot = bot
        default_member = {
            "League": None,
            "About": None,
        }
        default_guild = {
            "db": []
        }
        self.config = Config.get_conf(self, identifier=690830666, force_registration=True)
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)
    
    @commands.command(name="infohell", no_pm=True)
    async def infohell(self, ctx, user : discord.Member=None):
        """Check yours or someone's profile"""
                    
        server = ctx.guild
        db = await self.config.guild(server).db()
        user = user if user else ctx.author
        userdata = await self.config.member(user).all()
        data = discord.Embed(description="Still heavily in alpha version, all data will NOT be preserved.", colour=0xff0000)
        fields = [data.add_field(name=k, value=v) for k,v in userdata.items() if v]
        crncy = await bank.get_currency_name(ctx.guild)
        bal = await bank.get_balance(user)

        if user.id in db:
            name = str(user)
            name = " a.k.a. ".join((name, user.nick)) if user.nick else name
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
            data.add_field(name="Bank", value="Currently has **{} {}**".format(bal, crncy))
            await ctx.send(embed=data)
        else:
            db.append(user.id)
            await self.config.guild(server).db.set(db)
            name = str(user)
            name = " a.k.a. ".join((name, user.nick)) if user.nick else name
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
            data.add_field(name="Bank", value="Currently has **{} {}**".format(bal, crncy))
            await ctx.send(embed=data)

            
    @commands.group(name="iupdate", no_pm=True)
    async def iupdate(self, ctx):
        """Update the things in your profile"""
        pass

    @iupdate.command(pass_context=True, no_pm=True)
    async def about(self, ctx, *, about):
        """Tell us about yourself. Or type in some bullshit, I don't care"""
        
        server = ctx.guild
        user = ctx.author
        db = await self.config.guild(server).db()
        
        if user.id in db:
            await self.config.member(user).About.set(about)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name="Wooooo",value="You have updated your About Me: \n\n'**{}**'".format(about))
            await ctx.send(embed=data)
        else:
            db.append(user.id)
            await self.config.guild(server).db.set(db)
            await self.config.member(user).About.set(about)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name="Wooooo",value="You have updated your About Me: \n\n'**{}**'".format(about))
            await ctx.send(embed=data)

    @iupdate.command(pass_context=True, no_pm=True)
    async def lolname(self, ctx, *, ignleague):
        """Set your league name so you can show it to others with !!infohell. You know, cause of those symbols and shit. Looking at you, Mυfasa"""
        
        server = ctx.guild
        user = ctx.message.author
        db = await self.config.guild(server).db()

        if user.id in db:
            await self.config.member(user).League.set(ignleague)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name="Wooooooo",value="You have set your League name to: \n\n'**{}**".format(ignleague))
            await ctx.send(embed=data)
        else:
            db.append(user.id)
            await self.config.guild(server).db.set(db)
            name = str(user)
            name = " a.k.a. ".join((name, user.nick)) if user.nick else name
            await self.config.member(user).League.set(ignleague)
            data = discord.Embed(colour=0xff0000)
            data.add_field(name="Wooooooo",value="You have set your League name to: \n\n'**{}**".format(ignleague))
            await ctx.send(embed=data)

    @commands.command(name="lolname", no_pm=True)
    async def _lolname(self, ctx, user : discord.Member=None):
        """Outputs user's League nickname, if set with `!!update lolname`"""
        
        server = ctx.guild
        db = await self.config.guild(server).db()
        user = user if user else ctx.author
        name = str(user.display_name)
        userdata = await self.config.member(user).all()
        loluser = userdata['League']
        lolimg = ("http://www.macupdate.com/images/icons256/47210.png")
        data = discord.Embed(description="Summoner name:", colour=0xff0000)
        if user.id in db:
            aname = "'s ".join((name, "info"))
            data.set_author(name=aname, url=user.avatar_url)
            data.set_thumbnail(url=lolimg)
            data.add_field(name=(f"\n{loluser}"), value=u'\u200b')
            await ctx.send(embed=data)
        else:
            db.append(user.id)
            await self.config.guild(server).db.set(db)
            aname = "'s ".join((name, "info"))
            data.set_author(name=aname, url=user.avatar_url)
            data.set_thumbnail(url=lolimg)
            data.add_field(name=(f"\n{loluser}"), value=u'\u200b')
            await ctx.send(embed=data)
        
    @checks.admin_or_permissions(administrator=True)
    @commands.command(name="infowipe", no_pm=True)
    async def _infowipe(self, ctx):
        """Do not do that."""
        await ctx.send(f"You are about to wipe all the shit. "
                       f"\n\nIf you're sure you know what the fuck you're doing, type **{ctx.prefix}yes**. \n\n\n\nOtherwise - stay on the line for 20 seconds. Or type **{ctx.prefix}no** / **{ctx.prefix}cancel**.")
        choices = (f"{ctx.prefix}yes", f"{ctx.prefix}no", f"{ctx.prefix}cancel")
        check = lambda m: (m.author == ctx.author and m.channel == ctx.channel and m.content in choices)
        try:
            choice = await ctx.bot.wait_for("message", timeout=20.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Welp, since you didn't respond wipe is cancelled.")
        if choice.content.lower() == f"{ctx.prefix}yes":
            await self.config.clear_all_guilds()
            await self.config.clear_all_members()
            return await ctx.send("Data has been wiped.")
        else:
            return await ctx.send("Data wipe has been cancelled.")
            
    @commands.command()
    async def avatar(self, ctx, *, user: discord.User=None):
        """Provides user's avatar, name, nickname and role color."""
        if user is None:
            user = ctx.author
        if user.is_avatar_animated():
            av = user.avatar_url_as(format="gif")
        else:
            av = user.avatar_url_as(format="png")
        dnname = user.display_name
        dcolor = user.colour
        avembed = discord.Embed(colour=15158332)
        av = user.avatar_url
        avstr = str(av)
        avdesc = (f"[Click view it your in browser]({avstr}) \n\nUsername: {user}\nNickname: {dnname}\nRole color: {dcolor}")
        avembed.description = avdesc
        avembed.url = avstr
        avembed.set_image(url=avstr)
        avembed.set_footer(text="Powered by HELL")
        await ctx.send(embed=avembed)