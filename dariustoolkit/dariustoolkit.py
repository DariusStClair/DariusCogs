# Discord
import discord
# Red
from discord import Message, message
from redbot.core import checks, Config, commands
from redbot.core.utils.chat_formatting import bold, box, inline
# Libs

footer = "Powered by HELL"

class Hvhtools(commands.Cog):
    """Tools for a few communities"""

    def __init__(self, bot):
        self.bot = bot

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

    @checks.is_admin_or_superior()
    @commands.group(autohelp=True)
    async def vg(self, ctx):
        """Various tools for VG"""
        pass

    @checks.is_admin_or_superior()
    @hvh.command()
    async def assignroles(self, ctx):
        """Embeds the the assign roles list"""
        emoji_eune = "<:vg_eune:452893495921737728>"
        emoji_euw = "<:vg_euw:452893505778483201> "
        emoji_top = "<:vg_top:452893972688404491> "
        emoji_jungle = "<:vg_jungle:452893985107869737> "
        emoji_mid = "<:vg_mid:452893993219391509> "
        emoji_adc = "<:vg_adc:452894007509385216> "
        emoji_supp = "<:vg_supp:452895441961615383> "
        emoji_fill = "<:vg_fill:452893957215485953> "
        emoji_csgo = "<:CSGOlogo:534489391557509141> "
        emoji_fortnite = "<:si_fortnite:550324854532866088> "
        emoji_mc = "<:minecraft:513431092834074625> "
        emoji_pubg = "<:si_pubg:550324853836611585> "
        emoji_wc3 = "<:wc3:629302335880822814> "
        emoji_wow = "<:WoW:534489368228921354>"
        emoji_tft = "<:tft_icon:594189213222699009>"
        emoji_blank = "<:blank:438114864003809290>"
        emen = discord.Embed(colour=15158332, description="Реактнете със съответното емоджи за да получите/премахнете съответната роля.")
        emen.add_field(name="Изберете регион (или два)", value=f"EUNE - {emoji_eune}{emoji_blank}EUW - {emoji_euw}{emoji_blank}", inline=true)
        emen.add_field(name="Изберете предпочитаните ви роли", value=f"Top - {emoji_top}{emoji_blank}Jungle - {emoji_jungle}{emoji_blank}Mid - {emoji_mid}{emoji_blank}\nADC - {emoji_adc}{emoji_blank}Support - {emoji_supp}{emoji_blank}Fill - {emoji_fill}{emoji_blank}", inline=true)
        emen.add_field(name="Изберете игрите, които играете", value=f"CS:GO - {emoji_csgo}{emoji_blank}Fortnite - {emoji_fortnite}{emoji_blank}Minecraft - {emoji_mc}{emoji_blank}", inline=False)
        emen.add_field(name=u'\u200b', value=f"PUBG - {emoji_pubg}{emoji_blank}WarCraft III - {emoji_wc3}{emoji_blank}WoW - {emoji_wow}{emoji_blank}Teamfight Tactics - {emoji_tft}{emoji_blank}", inline=False)
        emen.set_footer(text=footer)
        await ctx.send(embed=emen)