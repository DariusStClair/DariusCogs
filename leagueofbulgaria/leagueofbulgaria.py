import discord
from typing import Optional, Union
from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import pagify, box, escape, text_to_file
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS, start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
import asyncio
import random
from io import BytesIO


class Leagueofbulgaria(commands.Cog):
    """
    Some shite
    """
    __author__ = ["Darius"]
    __version__ = "0.0.2"

    def __init__(self, bot):
        self.bot = bot
        def_member = {
            "Name": None,
        }
        def_guild = {
            "db": []
        }
        self.conf = Config.get_conf(self, 100068100001, force_registration=True)
        self.footer = f"Powered by Entropy | Version: {self.__version__}"
        self.conf.register_member(**def_member)
        self.conf.register_guild(**def_guild)

    def format_help_for_context(self, ctx):
        """Thanks to Sinbad wooo"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def _getmember(self, guild, search) -> Optional[discord.Member]:
        member = discord.utils.get(guild.members, id=search)
        return member

    @checks.mod_or_permissions(administrator=True)
    @commands.group(name="lob", no_pm=True)
    async def lob(self, ctx):
        """Основната League of Bulgaria командна група"""
        pass

    @checks.is_owner()
    @lob.command(name="dropdb")
    async def dropdb(self, ctx):
        """[Owner] Erase the entire DB"""
        await self.conf.clear_all_members()
        await self.conf.clear_all_guilds()
        await ctx.send("> Welp, all the data is now gone, gj {}".format(ctx.author.mention))

    @checks.is_owner()
    @lob.command(name="db")
    async def senddb(self, ctx):
        """[Owner] Изпраща текстов файл с базата данни"""
        fp = BytesIO()
        file = None
        author = ctx.author
        server = ctx.guild
        db = await self.conf.guild(server).db()
        userscount = 0
        userslist = []
        for i in db:
            tempuser = await self._getmember(server, i)
            userscount += 1
            userslist.append(tempuser)
        if userscount == 0:
            await ctx.send("DB is empty, {}".format(author.mention))
        else:
            slist = sorted(userslist, key=lambda x: getattr(x, "name"))
            astring = ""
            for user in userslist:
                nname = await self.conf.member(user).Name()
                astring += "{};{}\n".format(user, nname)
            await ctx.send(file=text_to_file(astring, filename="db.txt", spoiler=False), content="> Mi na ti pyk :D")

    @checks.is_owner()
    @lob.command(name="testid")
    async def testid(self, ctx, userid: int):
        """[Owner] zzz"""
        memb = await self._getmember(guild=ctx.guild, search=userid)
        em = discord.Embed(color=ctx.author.colour)
        if memb:
            em.description = "{}".format(memb.mention)
        else:
            em.description = "No such user. ({})".format(userid)
        em.set_footer(text="{}".format(self.footer))
        await ctx.send(embed=em)

    @checks.mod_or_permissions(administrator=True)
    @commands.guild_only()
    @lob.command(name="check", aliases=["checks", "exists", "added"])
    async def check(self, ctx, user: discord.Member = None):
        """Проверява дали някой потребител е в базата данни"""
        author = ctx.author
        server = ctx.guild
        db = await self.conf.guild(server).db()
        if not user:
            user = author
        if user.id in db:
            name = await self.conf.member(user).Name()
            em = discord.Embed(color=author.colour)
            em.add_field(name="{}'s nickname:".format(user.display_name), value="**{}**".format(name))
            em.set_footer(text="Requested by {} | {}".format(author, self.footer))
            em.set_author(name="{}: {}".format(user.display_name, name), icon_url=user.avatar_url)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(color=author.colour)
            em.add_field(name="{} **не е регистриран.**".format(user.display_name), value="За да се регистрирате прочетете условията в <#{}>.".format("691660302604828722"))
            em.set_footer(text="Requested by {} | {}".format(author, self.footer))
            em.set_author(name="{}".format(user.display_name), icon_url=user.avatar_url)
            await ctx.send(embed=em)

    @checks.mod_or_permissions(administrator=True)
    @commands.guild_only()
    @lob.command(name="add", aliases=["edit", "upd", "update"])
    async def addtodb(self, ctx, user: discord.Member, *, name: str):
        """
        Добавя потребител към базата данни.
        Формата е `!!lob add <@user> <nickname>`.
        """
        author = ctx.author
        server = ctx.guild
        db = await self.conf.guild(server).db()
        if user.id in db:
            await self.conf.member(user).Name.set(name)
            em = discord.Embed(color=author.colour)
            em.add_field(name="Nickname changed", value="Ника на {} вече е **{}**.".format(user.mention, name))
            em.set_footer(text="Changed by {} | {}".format(author, self.footer))
            em.set_author(name="{}: {}".format(user.display_name, name), icon_url=user.avatar_url)
        else:
            db.append(user.id)
            await self.conf.guild(server).db.set(db)
            await self.conf.member(user).Name.set(name)
            em = discord.Embed(color=author.colour)
            em.add_field(name="Nickname added", value="{} е добавен с никнейм **{}**.".format(user.mention, name))
            em.set_footer(text="Added by {} | {}".format(author, self.footer))
            em.set_author(name="{}: {}".format(user.display_name, name), icon_url=user.avatar_url)
        await ctx.send(embed=em)

    @checks.mod_or_permissions(administrator=True)
    @commands.guild_only()
    @lob.command(name="remove", aliases=["delete", "del", "rem"])
    async def removefromdb(self, ctx, user: discord.Member):
        """
        Премахва потребител от базата данни.
        Формата е `!!lob remove <@user>`
        """
        author = ctx.author
        server = ctx.guild
        db = await self.conf.guild(server).db()
        if user.id in db:
            await self.conf.member(user).Name.clear()
            db.remove(user.id)
            await self.conf.guild(server).db.set(db)
            em = discord.Embed(color=author.colour)
            em.add_field(name="Nickname removed", value="{} беше премахнат от базата данни.".format(user.mention))
            em.set_footer(text="Removed by {} | {}".format(author, self.footer))
            em.set_author(name="Removed {}".format(user.display_name), icon_url=user.avatar_url)
        else:
            em = discord.Embed(color=author.colour)
            em.add_field(name="Not found", value="{} не съществува в базата данни.".format(user.mention))
            em.set_footer(text="Attempted by {} | {}".format(author, self.footer))
            em.set_author(name="Couldn't find {}".format(user.display_name), icon_url=user.avatar_url)
        await ctx.send(embed=em)
    
    @checks.mod_or_permissions(administrator=True)
    @commands.guild_only()
    @lob.command(name="list", aliases=["lst", "show", "all", "showall"])
    async def listdb(self, ctx):
        """
        Предоставя лист с всички потребители в базата данни до момента.
        """
        author = ctx.author
        server = ctx.guild
        db = await self.conf.guild(server).db()
        userscount = 0
        userslist = []
        for i in db:
            tempuser = await self._getmember(server, i)
            userscount += 1
            userslist.append(tempuser)
        if userscount == 0:
            await ctx.send("DB is empty, {}".format(author.mention))
        else:
            slist = sorted(userslist, key=lambda x: getattr(x, "mention"))
            astring = ""
            for user in userslist:
                nname = await self.conf.member(user).Name()
                astring += "▫️ {}: **{}**\n".format(user.mention, nname)
            embed_list = []
            pg_count = 0
            for page in pagify(astring, delims=["\n"], page_length=400):
                pg_has = page.count("▫️")
                pg_count = pg_count + pg_has
                title = "До момента базата данни съдържа:"
                em = discord.Embed(description=page, color=author.colour)
                em.set_footer(text="Showing {}/{} | {}".format(pg_count, userscount, self.footer))
                em.set_author(name=title)
                embed_list.append(em)
            if len(embed_list) == 1:
                return await ctx.send(embed=em)
            await menu(ctx, embed_list, DEFAULT_CONTROLS)


