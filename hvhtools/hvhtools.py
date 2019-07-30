# Discord
import discord
# Red
from discord import Message, message
from redbot.core import checks, Config, commands
from redbot.core.utils.chat_formatting import bold, box, inline
# Libs

footer = "Powered by HELL"

class Hvhtools(commands.Cog):
    """Tools for the HVH community"""

    def __init__(self, bot):
        self.bot = bot

    @checks.guildowner()
    @commands.group(autohelp=True)
    async def hvh(self, ctx):
        """Various tools for the HVH community"""
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
        """Embeds the rules in: **Russian**"""
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
        """Embeds the rules in: **Bulgarian**"""
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
    async def links(self, ctx, linkru = None, linkbg = None, linken = None):
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
        embed.add_field(name=":flag_ru:", value=emgru)
        embed.add_field(name=":flag_bg:", value=embg)
        embed.add_field(name=":flag_us:", value=emen)
        embed.set_footer(text=footer)
        await ctx.send (embed=embed)