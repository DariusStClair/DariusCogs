# Ugh I gotta start using notes and shit
import discord
# Red stuffs
from redbot.core import checks, Config, bank, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils import mod
from redbot.core.utils.chat_formatting import bold, box, inline
# Libs
import asyncio
import datetime
import random
import calendar

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
        self.randomfuckingcat = [
            "https://cdn.discordapp.com/attachments/610443480493457408/625244252699361280/1.gif",
            "https://cdn.discordapp.com/attachments/610443480493457408/625244253911646228/2.gif",
            "https://cdn.discordapp.com/attachments/610443480493457408/625244255870255104/3.gif",
            "https://cdn.discordapp.com/attachments/610443480493457408/625244256910442496/4.gif",
            "https://cdn.discordapp.com/attachments/610443480493457408/625244258676375562/5.gif",
            "https://cdn.discordapp.com/attachments/610443480493457408/625244260945494017/6.gif",
            "https://cdn.discordapp.com/attachments/610443480493457408/625244263411875851/7.gif"
        ]
    
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

            
    @commands.command(name="meow", no_pm=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def meow(self, ctx):
        await ctx.send(file=discord.File(random.choice(self.randomfuckingcat), "zemimeow.gif"))
        
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

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def nofucks(self, ctx):
        user = ctx.author
        if user.is_avatar_animated():
            av = user.avatar_url_as(format="gif")
        else:
            av = user.avatar_url_as(format="png")
        dnname = user.display_name
        em = discord.Embed(colour=15158332)
        av = user.avatar_url
        avstr = str(av)
        img = "https://perpetualabsurdity.files.wordpress.com/2015/12/6npyrf2.jpg"
        avdesc = (f"**Behold! The field in which I grow my fucks.**\n\n**Lay thine eyes upon it and thou shalt see that it is barren.**")
        em.description = avdesc
        em.url = img
        em.set_image(url=img)
        em.set_author(name=f"{dnname}", url=f"{avstr}", icon_url=f"{avstr}")
        em.set_footer(text=f"Powered by HELL")
        await ctx.send(embed=em)
