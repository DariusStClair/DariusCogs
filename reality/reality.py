import discord
from redbot.core import Config, commands, checks
from typing import Optional, Union
import datetime
import time
from redbot.core.utils.chat_formatting import bold, box, inline
import random
import asyncio

from .repl import RCHECK, STEPS, NOTYET, RULESK, RULESV, ALLROLES, ALLROLESDESCR

class Reality(commands.Cog):
    """
    Reality is not digital, an on-off state, but analog. Something gradual. 
    In other words, reality is a quality that things possess in the same way that they possess, say, weight. Some people are more real than others, for example. 
    """
    default_global_settings = {"m_list": [],
    }
    default_user_settings = {
        "ENABLED": False,
        "THINGS": {},
    }

    def __init__(self, bot):
        self.bot = bot
        self._config = Config.get_conf(self, 6660426660, force_registration=True)
        self._config.register_global(**self.default_global_settings)
        self._config.register_user(**self.default_user_settings)
        self._version = "1.00.0"
        self._memeh = "https://meme-api.herokuapp.com/"
        self.bot.remove_command("ping")

    @commands.command()
    async def ping(self, ctx):
        realitycheck = ctx.bot.get_command("reality check")
        await ctx.invoke(realitycheck)

    @commands.group(name="void", aliases=["v"], no_pm=True)
    @commands.is_owner()
    async def voidgroup(self, ctx):
        """This is meant for the void server only really"""
        pass

    @checks.mod_or_permissions(manage_messages=True)
    @checks.bot_has_permissions(manage_messages=True, send_messages=True)
    @voidgroup.group(name="rules", aliases=["rule", "r"], no_pm=True, autohelp=False)
    async def voidrules(self, ctx, thingy: Union[int, str] = None):
        """Group for the rules under `void`"""
        await ctx.message.delete()
        rk, rv = RULESK, RULESV
        validrange = {
            "pride": 1, 
            "gluttony": 2,
            "lust": 3,
            "greed": 4,
            "envy": 5,
            "wrath": 6,
            "sloth": 7,
        }
        if not thingy:
            eyemoji = discord.utils.get(self.bot.emojis, id=683092923415396363)
            em = discord.Embed(colour=0x7700aa, description=box("Or as people often call them - rules.\nMake sure you've read them and you're familiar with all of this. It's your own responsibility."), title="{} The seven (deadly?) sins".format(eyemoji))
            em.set_footer(text="Powered by Entropy")
            em.set_author(name="{}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
            for i in rk:
                em.add_field(name="\N{ZERO WIDTH SPACE}", value="**{}**\n{}".format(rk[i], rv[i]), inline=False)
            await ctx.send(embed=em)
            return
        if type(thingy) is int:
            if 1 <= thingy <= 8:
                eyemoji = discord.utils.get(self.bot.emojis, id=683092923415396363)
                em = discord.Embed(colour=0x7700aa, title="{} The seven (deadly?) sins: Sin #{}".format(eyemoji, thingy))
                em.set_footer(text="Requested by {} | Powered by Entropy".format(ctx.author.name))
                em.set_author(name="{}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                em.add_field(name="\N{ZERO WIDTH SPACE}", value="**{}**\n{}".format(rk[thingy], rv[thingy]), inline=False)
                await ctx.send(embed=em)
                return
        if type(thingy) is str:
            lthingy = thingy.lower()
            cthingy = lthingy.capitalize()
            if lthingy in validrange:
                eyemoji = discord.utils.get(self.bot.emojis, id=683092923415396363)
                em = discord.Embed(colour=0x7700aa, title="{} The seven (deadly?) sins: Sin #{}, {}".format(eyemoji, validrange[lthingy], cthingy))
                em.set_footer(text="Requested by {} | Powered by Entropy".format(ctx.author.name))
                em.set_author(name="{}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                em.add_field(name="\N{ZERO WIDTH SPACE}", value="**{}**\n{}".format(rk[validrange[lthingy]], rv[validrange[lthingy]]), inline=False)
                await ctx.send(embed=em)
                return
        eyemoji = discord.utils.get(self.bot.emojis, id=683092923415396363)
        em = discord.Embed(colour=0x7700aa, title="{} That's not a valid sin.".format(eyemoji, thingy))
        em.set_footer(text="Requested by {} | Powered by Entropy".format(ctx.author.name))
        em.set_author(name="{}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
        await ctx.send(embed=em)


    @checks.mod_or_permissions(manage_messages=True)
    @checks.bot_has_permissions(manage_messages=True, send_messages=True)
    @voidgroup.group(name="role", aliases=["roles"], no_pm=True, autohelp=False)
    async def voidroles(self, ctx):
        rolek, rolev = ALLROLES, ALLROLESDESCR
        em = discord.Embed(colour=0x7700aa, description=box("Get your own roles here!\nReact/unreact to respectively get/remove a role."), title="Role settings")
        em.set_footer(text="Powered by Entropy")
        em.set_author(name="{}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
        for i in rolek:
            em.add_field(name="\N{ZERO WIDTH SPACE}", value="**{}**\n{}".format(rolek[i], rolev[i]), inline=False)
        await ctx.send(embed=em)

    @commands.group(name="reality", aliases=["r"], no_pm=True)
    async def reality(self, ctx):
        """
        Reality is not digital, an on-off state, but analog. Something gradual. 
        In other words, reality is a quality that things possess in the same way that they possess, say, weight. Some people are more real than others, for example. 
        """
        pass

    @reality.command(name="check", aliases=["ping", "p", "c"], no_pm=True)
    @commands.cooldown(rate=3, per=10, type=commands.BucketType.user)
    async def check(self, ctx):
        """It's really just a ping."""
        phrases = RCHECK
        maxp = len(phrases) - 1
        repl = phrases[random.randint(0, maxp)]
        latency = self.bot.latency * 1000
        tping = "..."
        em = discord.Embed(colour=0x36393f, description="{}".format(repl), set_footer="Powered By Entropy")
        em.add_field(name="Discord responded in:", value=box("{} ms".format(latency)), inline=False)
        em.add_field(name="Calculating typing:", value=box("{}".format(tping)), inline=False)
        before = time.monotonic()
        msg = await ctx.send(embed=em)
        tlatency = (time.monotonic() - before) * 1000
        em = discord.Embed(colour=0x36393f, description="{}".format(repl), set_footer="Powered By Entropy")
        em.add_field(name="Discord responded in:", value=box("{} ms".format(latency)), inline=False)
        em.add_field(name="Calculated typing:", value=box("{} ms".format(tlatency)), inline=False)
        await msg.edit(embed=em)

    @commands.command(name="step", aliases=["стъпка"], no_pm=True, autohelp=False)
    @commands.cooldown(3, 3, commands.BucketType.guild)
    async def step(self, ctx, number: Optional[int] = 0):
        """Step 1 is usually good. But y no try others?"""
        list1c = [186282, 299792, 299792458, 670616629, 1079251200]
        phrases = NOTYET
        maxp = len(phrases) - 1
        if number <= 0:
            await ctx.send(STEPS[0].format(ctx.prefix))
            return
        if number in STEPS and number < 9000 or number in list1c:
            if number == 9:
                emoji = discord.utils.get(self.bot.emojis, id=670724388370382873)
                await ctx.send("{} {}".format(STEPS[number], emoji))
                return
            elif number == 26:
                emoji = discord.utils.get(self.bot.emojis, id=356913591951032332)
                await ctx.send("{} {}".format(emoji, STEPS[number]))
                return
            else:
                await ctx.send(STEPS[number])
                return
        if number > 8999:
            await ctx.send(STEPS[9001])
            return
        else:
            repl = phrases[random.randint(0, maxp)]
            await ctx.send(repl)

    @commands.command(name="stepscount", no_pm=True)
    async def stepscount(self, ctx):
        await ctx.send(len(STEPS))