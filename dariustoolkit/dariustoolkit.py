# Discord
import discord
# Red
from discord import Message, message
from redbot.core import checks, Config, commands
from redbot.core.utils.chat_formatting import bold, box, inline
# Libs
import random
import asyncio
from PIL import Image


footer = "Powered by Entropy"

class Dariustoolkit(commands.Cog):
    """Tools for a few communities"""

    def __init__(self, bot):
        self.bot = bot
        self.membahs = None

    async def _emoji(self, name):
        emoji = "<:blank_empty:595739688237662210>"
        for n_ in self.bot.emojis:
            if n_.name == name:
                emoji = f"<:{n_.name}:{n_.id}>"
        return emoji

    async def _randshit(self, int):
        r = random.uniform(0.3, int)
        return r

    async def _randshitslow(self, int):
        r = random.uniform(1.5, int)
        return r
    
    async def _randshitslower(self, int):
        r = random.uniform(2, int)
        return r

    async def _randmembers(self, guild, aint):
        if self.membahs is None:
            membahs = await self._updmembahs(guild)
        raint = []
        for i in range(1, aint):
            r = random.choice(membahs)
            raint.append(r)
            membahs.remove(r)
        return raint

    async def _updmembahs(self, guild):
        membahs = []
        for i in range(len(guild.members)):
            membahs.append(guild.members[i])
        return membahs

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
    @commands.cooldown(1, 120, commands.BucketType.default)
    async def vc(self, ctx):
        guild = ctx.guild
        p_names = ["Alfa", "Beta", "Gamma", "Delta", "Epsilon", "Vafli", "Putkimaini", "Lyutenitsa", "GoldenRetriever", "Omega", "ugh whatever"]
        p_numbers = [" I ARE VC WE ALO VC??", " VC VC VC VC", " VC!!!", " VC???", " so yeah, move on", " POWERFUL STRONG FORCE!!!", " x84", " - 984.1804", "-0000000000001", "-93", ", I think", "!!!1!!!1!!!", "_?????!??", " and shit", " - i4i1kjng", " 9301", " v1.3", " v0.83a", "_TJ019tujUJJUERJg", "-PP22", "/69.420", ".3.35"]
        p_name = random.choice(p_names)
        p_number = random.choice(p_numbers)
        randprotocol = f"**{p_name}" + f"{p_number}**"
        em = discord.Embed(colour=0x36393f, description="**Dido2 VC Mode activated!!!1!**")
        em.set_footer(text="Powered by Entropy | VC ANYONE?! | VC????? | VC!!!!!!1!!!!1!!!")
        thingy = await ctx.send(embed=em)
        rand_slow = await self._randshit(3)
        await asyncio.sleep(rand_slow)
        em = discord.Embed(colour=0x36393f, description="**Dido2 VC Mode activated!!!1!**\n\n")
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading", inline=False)
        await thingy.edit(embed=em)
        rand_fast = await self._randshit(1)
        await asyncio.sleep(rand_fast)
        em.clear_fields()
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . ", inline=False)
        await thingy.edit(embed=em)
        rand_fast = await self._randshit(2)
        await asyncio.sleep(rand_fast)
        em.clear_fields()
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . . ", inline=False)
        await thingy.edit(embed=em)
        rand_fast = await self._randshit(3)
        await asyncio.sleep(rand_fast)
        em.clear_fields()
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . . . done!", inline=False)
        await thingy.edit(embed=em)
        # protocol shit
        wait = await self._randshitslow(3)
        await asyncio.sleep(wait)
        em.clear_fields()
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . . . done!", inline=False)
        em.add_field(name=f"Connection to VC:", value=f"[░░░░░░░░░░   0%]", inline=False)
        await thingy.edit(embed=em)
        wait = await self._randshitslow(2)
        await asyncio.sleep(wait)
        em.clear_fields()
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . . . done!", inline=False)
        randnumb = random.randint(10, 20)
        em.add_field(name=f"Connection to VC:", value=f"[▓▓░░░░░░░░  {randnumb}%]", inline=False)
        await thingy.edit(embed=em)
        wait = await self._randshitslow(5)
        await asyncio.sleep(wait)
        em.clear_fields()
        randnumb = random.randint(40, 49)
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . . . done!", inline=False)
        em.add_field(name=f"Connection to VC:", value=f"[▓▓▓▓▓░░░░░  {randnumb}%]", inline=False)
        await thingy.edit(embed=em)
        wait = await self._randshitslow(4)
        await asyncio.sleep(wait)
        em.clear_fields()
        randnumb = random.randint(55, 69)
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . . . done!", inline=False)
        em.add_field(name=f"Connection to VC:", value=f"[▓▓▓▓▓▓▓░░░  {randnumb}%]", inline=False)
        await thingy.edit(embed=em)
        wait = await self._randshitslow(3)
        await asyncio.sleep(wait)
        em.clear_fields()
        randnumb = random.randint(88, 99)
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . . . done!", inline=False)
        em.add_field(name=f"Connection to VC:", value=f"[▓▓▓▓▓▓▓▓▓░  {randnumb}%]", inline=False)
        await thingy.edit(embed=em)
        wait = await self._randshitslow(2)
        await asyncio.sleep(wait)
        em.clear_fields()
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . . . done!", inline=False)
        em.add_field(name=f"Connection to VC:", value=f"[▓▓▓▓▓▓▓▓▓▓ 100%] ESTABLISHED!", inline=False)
        await thingy.edit(embed=em)
        ###
        wait = await self._randshitslow(2)
        await asyncio.sleep(wait)
        em.clear_fields()
        randtar1 = "Searching..."
        randtar2 = randtar1
        randtar3 = randtar1
        randtar4 = randtar1
        em.add_field(name=f"Initialting protocol: {randprotocol}", value=f"⁣                    ⁣Loading . . . done!", inline=False)
        em.add_field(name=f"Connection to VC:", value=f"[▓▓▓▓▓▓▓▓▓▓ 100%] ESTABLISHED!", inline=False)
        em.add_field(name=f"\n**Commencing annoyance of random people!**", value=f"But I'm not gonna tag them, you do that.", inline=False)
        await thingy.edit(embed=em)
        ### picks
        wait = await self._randshitslow(4)
        maxt = 5
        randtars = await self._randmembers(guild, maxt)
        step = 0
        for i in range(0, maxt):
            targetn = i + 1
            em.add_field(name=f"*Target {targetn}:*", value=f"**{randtars[step]}**", inline=False)
            step += 1
            waitz = await self._randshitslow(4)
            await asyncio.sleep(waitz)
            await thingy.edit(embed=em)

    @checks.guildowner()
    @commands.group(autohelp=True)
    async def fpx(self, ctx):
        """Tools for the FPX Community"""
        pass

    @checks.guildowner()
    @fpx.command()
    async def rulestest(self, ctx, chan: discord.TextChannel=None):
        guild = ctx.guild
        if chan is None:
            chan = ctx.channel
        emptyf = u'\u200b'
        v1 = '''__***1. Правила за всички гласови канали***__

**1.1.** Забранени силни, досадни звуци, викове, voice changers (както и всякакъв вид пречене на нормална комуникация).
```yaml
Наказание - Mute за 240 минути + Warn```

**1.2.** Неподходящото поведение във всякакви прояви е забранено (обиди, викове, провокации и всичко свързано с неподходящо поведение).
```yaml
Наказание - Muteдо 60 минути```

**1.3.** Обидите, провокациите към администрацията са забранени. 
```yaml
Наказание - Mute за 120 минути```'''

        v2 = '''__***2. Правила за всички текстови канали***__

**2.1.** Неспазването на темите за чат е забранено.

**2.3.** Във всички чатове са забранени обиди и провокации от всякакъв вид.
```yaml
Наказание по преценка на администрацията```

**2.4.** Забранено е публикуването на NSFW съдържание (като разчленяване, порнография и т.н.) във всички чатове, освен маркираните като NSFW.
```yaml
Наказание Mute за 360 минути + Warn```

**2.5.** Забранено е да се споменават всички свързани роли без причина. Честото споменаване на ролите също е забранено.
```yaml
Наказание Mute за 120 минути + Warn```'''
        v3 = '''__***3. Забрани за конкретни действия***__

**3.1.** Търговската дейност на сървъра е забранена, ако нямате изрично разрешение от <@&641724084862058516>.
```yaml
Наказание - по преценка на администрацията```

**3.2.** Забранено е използването на каквито и да е уязвимости за получаване на всякакъв вид ползи под каквато и да е форма, както и да се вземе музикален бот, когато се използва.
```yaml
Наказание - по преценка на администрацията```

**3.3.** Реклама на лични акаунти, телефонни номера, съвъри, скрийншоти с покана, изпращане на лично съобщение.
```yaml
Наказание - по преценка на администрацията```

**3.4.** Забранява се умишлено копиране на профили.
```yaml
Първо предупреждение, следващо наказание - Warn```

**3.5.** Оспорването на действията на администрацията е забранено.
```yaml
Наказание - по преценка на администрацията```
'''
        v4 = '''__***4. Бележки***__

**4.1.** Правилата могат да се актуализират и допълват без предупреждение.

**4.2.** Прекомерното нарушаване на правилата на сървъра може да доведе до последствия.

Ако по преценка на <@&641721930457808946>, <@&641724084862058516> или <@&641721261612859433> вашите действия могат да навредят на сървъра или да причинят някаква вреда на участниците в проекта, тогава той има право да ви изрита от сървъра за определен период или да преустанови достъпа ви перманентно.

**4.3.** След като влезете в сървъра, вие автоматично се съгласявате и приемате правилата / позицията на сървъра.

__*Видове наказания*__

<@&652862554367983616> - Ролята забранява използването на всички гласови канали.

<@&652864798467293184> - Наказанието забранява достъпа до всички текстови и гласови канали.

**__Можете да обжалвате наказанието пред всеки от Модераторите, Control или Associate.__**\n
**При проблеми с <@&641721930457808946>, <@&641721675167301642> или <@&641721261612859433> се обръщайте към <@&641724084862058516>.**'''
        em1 = discord.Embed(colour=0x36393f, description=v1)
        em2 = discord.Embed(colour=0x36393f, description=v2)
        em3 = discord.Embed(colour=0x36393f, description=v3)
        em4 = discord.Embed(colour=0x36393f, description=v4)
        em4.set_footer(text=footer)
        await ctx.send(embed=em1)
        asyncio.sleep(2)
        await ctx.send(embed=em2)
        asyncio.sleep(2)
        await ctx.send(embed=em3)
        asyncio.sleep(2)
        await ctx.send(embed=em4)
        asyncio.sleep(1)
        await ctx.send(">>> **Done.**\n*(you can delete this message)*")

    @commands.command()
    async def atest(self, ctx, *, user: discord.User=None):
        """baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaah"""
        if user is None:
            user = ctx.author
        if user.is_avatar_animated():
            av = user.avatar_url_as(format="gif")
        else:
            av = user.avatar_url_as(format="png")

    @commands.command()
    async def thumbs(self, ctx, msg: int, channel: discord.TextChannel = None):
        if channel is None:
            chan = ctx.channel
        else:
            chan = channel
        message = await chan.fetch_message(msg)
        try:
            ru = next(filter(lambda x: x.emoji == '\U0001F44D', message.reactions), None)
            rd = next(filter(lambda x: x.emoji == '\U0001F44E', message.reactions), None)
        except AttributeError:
            return await ctx.send("> Well that failed. `(1)`")
        if ru is None:
            tusers = "Zero."
        else:
            tusers = await ru.users()
            for i in len(tusers):
                tup = ', '.join(tusers.name(i))
        if rd is None:
            tdsers = "Zero."
        else:
            tdsers = await rd.users()
            for i in len(tdsers):
                tup = ', '.join(tdsers.name(i))
        resp = f'Users that reacted with:\n 👍\n{tup}.\n\nUsers that reacted with:\n 👎\n{tdown}.'
        await ctx.send(resp)