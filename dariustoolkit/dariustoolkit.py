# Discord
import discord
# Red
from discord import Message, message
from redbot.core import checks, Config, commands
from redbot.core.utils.chat_formatting import bold, box, inline
# Libs
import random
import asyncio

footer = "Powered by HELL"

class Dariustoolkit(commands.Cog):
    """Tools for a few communities"""

    def __init__(self, bot):
        self.bot = bot

    async def _emoji(self, name):
        emoji = "<:blank_empty:595739688237662210>"
        for n_ in self.bot.emojis:
            if n_.name == name:
                emoji = f"<:{n_.name}:{n_.id}>"
        return emoji

    async def _randshit(self, int):
        r = random.uniform(0.3, int)
        return r

    @checks.guildowner()
    @commands.group(autohelp=True)
    async def hvh(self, ctx):
        """Various tools for HVH"""
        pass

    @hvh.command()
    async def rulesen(self, ctx):
        """Embeds the rules in: **English**"""
        emen = discord.Embed(colour=15158332, description=":flag_us:")
        emen.add_field(name="1. Be respectful and act civil.", value=u'\u200b', inline=False)
        emen.add_field(name="2. Use proper grammar and spelling and don't spam.", value=u'\u200b', inline=False)
        emen.add_field(name="3. (Optional)  Usage of excessive extreme inappropriate language is prohibited.", value=u'\u200b', inline=False)
        emen.add_field(name="4. Mentioning @everyone / @here, the @STAFF or a specific person without proper reason is prohibited.", value=u'\u200b', inline=False)
        emen.add_field(name="5. Post content in the correct channels.", value=u'\u200b', inline=False)
        emen.add_field(name="6. Don't post someone's personal information without permission.", value=u'\u200b', inline=False)
        emen.add_field(name="7. Listen to what Staff says.", value=u'\u200b', inline=False)
        emen.add_field(name="8. Do not post graphic pictures of minors (under 18).", value=u'\u200b', inline=False)
        emen.add_field(name="9. It's forbidden to have any links related to any exploits/hacks, including but not limited to DLLs, EXEs, injectors, grabbers etc. It will get you muted or banned.", value=u'\u200b', inline=False)
        emen.set_footer(text=footer)
        await ctx.send(embed=emen)

    @hvh.command()
    async def rulesru(self, ctx):
        """HVH: Embeds the rules in: **Russian**"""
        emen = discord.Embed(colour=15158332, description=":flag_ru:")
        emen.add_field(name="1. Будьте уважительны и действуйте вежливо.", value=u'\u200b', inline=False)
        emen.add_field(name="2. Используйте правильную грамматику и орфографию и не спамуйте.", value=u'\u200b', inline=False)
        emen.add_field(name="3. (Необязательно) Использование чрезмерного, крайне неуместного языка запрещено.", value=u'\u200b', inline=False)
        emen.add_field(name="4. Упоминание @everyone / @here, @STAFF или конкретного человека без уважительной причины запрещено.", value=u'\u200b', inline=False)
        emen.add_field(name="5. Публикуйте контент в нужных каналах.", value=u'\u200b', inline=False)
        emen.add_field(name="6. Не размещайте чью-либо личную информацию без разрешения.", value=u'\u200b', inline=False)
        emen.add_field(name="7. Послушайте, что говорит персонал.", value=u'\u200b', inline=False)
        emen.add_field(name="8. Не размещайте графические изображения несовершеннолетних (до 18 лет).", value=u'\u200b', inline=False)
        emen.add_field(name="9. Запрещено иметь какие-либо ссылки, связанные с какими-либо эксплойтами / взломами, включая, но не ограничиваясь, DLL, EXE, инжекторы, грабберы и т. Д. Это отключит вас или заблокирует.", value=u'\u200b', inline=False)
        emen.set_footer(text=footer)
        await ctx.send(embed=emen)

    @hvh.command()
    async def rulesbg(self, ctx):
        """HVH: Embeds the rules in: **Bulgarian**"""
        emen = discord.Embed(colour=15158332, description=":flag_bg:")
        emen.add_field(name="1. Дръжте се уважително и цивилизовано.", value=u'\u200b', inline=False)
        emen.add_field(name="2. Използвайте правилна граматика и правопис и не спамете.", value=u'\u200b', inline=False)
        emen.add_field(name="3. (Незадължително) Използването на прекомерно крайно неподходящ език е забранено.", value=u'\u200b', inline=False)
        emen.add_field(name="4. Споменаването на @everyone / @here, @STAFF или конкретно лице без основателна причина е забранено.", value=u'\u200b', inline=False)
        emen.add_field(name="5. Публикувайте съдържание в правилните канали.", value=u'\u200b', inline=False)
        emen.add_field(name="6. Не публикувайте нечия лична информация без разрешение.", value=u'\u200b', inline=False)
        emen.add_field(name="7. Слушайте какво казва персоналът.", value=u'\u200b', inline=False)
        emen.add_field(name="8. Не публикувайте графични снимки на непълнолетни лица (под 18 години).", value=u'\u200b', inline=False)
        emen.add_field(name="9. Забранено е да поствате  във всички канали  / хакове, включително, но не само, DLL файлове, EXE, инжектори, грабъри и т.н. Това ще се наказва със БАН или МЮТ.", value=u'\u200b', inline=False)
        emen.set_footer(text=footer)
        await ctx.send(embed=emen)
    @hvh.command()
    async def links(self, ctx, linken = None, linkru = None, linkbg = None):
        emgru = "[Нажмите здесь, чтобы перейти к правилам на русском языке.]"
        emgru += "("
        emgru += linkru
        emgru += ")"
        embg = "[Щракнете тук, за да преминете към правилата на български език.]"
        embg += "("
        embg += linkbg
        embg += ")"
        emen = "[Click here to jump to the rules in English.]"
        emen += "("
        emen += linken
        emen += ")"
        embed = discord.Embed(colour=15158332)
        embed.add_field(name=":flag_us:", value=emen)
        embed.add_field(name=":flag_ru:", value=emgru)
        embed.add_field(name=":flag_bg:", value=embg)
        embed.set_footer(text=footer)
        await ctx.send (embed=embed)

    @checks.guildowner()
    @commands.group(autohelp=True)
    async def vg(self, ctx):
        """Various tools for VG"""
        pass

    @vg.command()
    async def assignroles(self, ctx):
        """Embeds the the assign roles list"""
        emoji_eune = await self._emoji("vg_eune")
        emoji_euw = await self._emoji("vg_euw")
        emoji_top = await self._emoji("vg_top")
        emoji_jungle = await self._emoji("vg_jungle")
        emoji_mid = await self._emoji("vg_mid")
        emoji_adc = await self._emoji("vg_adc")
        emoji_supp = await self._emoji("vg_supp")
        emoji_fill = await self._emoji("vg_fill")
        emoji_csgo = await self._emoji("CSGOlogo")
        emoji_fortnite = await self._emoji("si_fortnite")
        emoji_mc = await self._emoji("minecraft")
        emoji_pubg = await self._emoji("si_pubg")
        emoji_wc3 = await self._emoji("wc3")
        emoji_wow = await self._emoji("WoW")
        emoji_tft = await self._emoji("tft_icon")
        emoji_blank = await self._emoji("blank_empty")
        emen = discord.Embed(colour=15158332, description="**__Реактнете със съответното емоджи за да получите/премахнете съответната роля.__**\n\nМожете да използвате например `@EUNE @Support` в <#451075658013999106> за да пингнете хората с тези роли.\nСъщо така в <#440434633390292993> можете да получите роли за съответните ви дивизии, така че по-лесно да бъдете намирани за ранкед игри.")
        emen.add_field(name="Изберете регион (или два) и предпочитаните ви роли:", value=f"{emoji_top}{emoji_blank}Top\n{emoji_jungle}{emoji_blank}Jungle\n{emoji_mid}{emoji_blank}Mid\n{emoji_adc}{emoji_blank}ADC\n{emoji_supp}{emoji_blank}Support\n{emoji_fill}{emoji_blank}Fill", inline=True)
        emen.add_field(name=u'\u200b', value=f"{emoji_eune}{emoji_blank}EUNE\n{emoji_euw}{emoji_blank}EUW", inline=True)
        emen.add_field(name="Изберете игрите, които играете:", value=f"{emoji_csgo}{emoji_blank}CS:GO\n{emoji_fortnite}{emoji_blank}Fortnite\n{emoji_mc}{emoji_blank}Minecraft\n{emoji_tft}{emoji_blank}Teamfight Tactics", inline=True)
        emen.add_field(name=u'\u200b', value=f"{emoji_pubg}{emoji_blank}PUBG\n{emoji_wc3}{emoji_blank}WarCraft III\n{emoji_wow}{emoji_blank}WoW\n", inline=True)
        emen.set_footer(text=footer)
        await ctx.send(embed=emen)

    @commands.command(name="vc", no_pm=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def vc(self, ctx):
        times = 4
        for i in range(0, times):
            randomtest = await self._randshit(1)
            await ctx.send(f">>> Randomtest {i}: {randomtest}")
        await ctx.send(">>> Done.")
