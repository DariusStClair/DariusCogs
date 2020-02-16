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
import numpy

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
        seq1 = {
            0: "Initialting protocol: {}\n⁣Loading",
            1: "Initialting protocol: {}\nLoading .",
            2: "Initialting protocol: {}\n⁣Loading . . ",
            3: "Initialting protocol: {}\n⁣Loading . . . done!"
        }
        seq2 = {
            0: "Connection to VC:\n[░░░░░░░░░░   0%]",
            1: "Connection to VC:\n[▓░░░░░░░░░  {}%]",
            2: "Connection to VC:\n[▓▓▓░░░░░░░  {}%]",
            3: "Connection to VC:\n[▓▓▓▓░░░░░░  {}%]",
            4: "Connection to VC:\n[▓▓▓▓▓░░░░░  {}%]",
            5: "Connection to VC:\n[▓▓▓▓▓▓░░░░  {}%]",
            6: "Connection to VC:\n[▓▓▓▓▓▓▓░░░  {}%]",
            7: "Connection to VC:\n[▓▓▓▓▓▓▓▓░░  {}%]",
            8: "Connection to VC:\n[▓▓▓▓▓▓▓▓▓░  {}%]",
            9: "Connection to VC:\n[▓▓▓▓▓▓▓▓▓▓ 100%] ESTABLISHED!\n**Commencing annoyance of random people!**"
        }
        em = discord.Embed(colour=0x36393f, description="**Dido2 VC Mode activated!!!1!**")
        em.set_footer(text="Powered by Entropy | VC ANYONE?! | VC????? | VC!!!!!!1!!!!1!!!")
        msg = await ctx.send(embed = em)
        n = 0
        k = 0
        for i in range(len(seq1)):
            em = discord.Embed(colour=0x36393f, description="**Dido2 VC Mode activated!!!1!**")
            em.set_footer(text="Powered by Entropy | VC ANYONE?! | VC????? | VC!!!!!!1!!!!1!!!")
            em.add_field(name="Working", value=seq1[n].format(randprotocol), inline=False)
            await asyncio.sleep(2)
            n += 1
            await msg.edit(embed=em)
        await asyncio.sleep(10)
        for i in range(len(seq2)):
            randint1 = k * 10
            randint2 = k * 10 + 10
            if k == 9:
                randint = 100
            else:
                randint = random.randint(randint1, randint2)
            em = discord.Embed(colour=0x36393f, description="**Dido2 VC Mode activated!!!1!**\nWorking\nInitializing protocol: **{}**\nLoading . . . done!".format(randprotocol))
            em.set_footer(text="Powered by Entropy | VC ANYONE?! | VC????? | VC!!!!!!1!!!!1!!!")
            em.add_field(name="Establishing communications", value=seq2[k].format(randint), inline=False)
            k += 1
            await asyncio.sleep(random.randint(2, 4))
            await msg.edit(embed=em)
        await asyncio.sleep(2)
        rmembers = []
        numbah = 0
        nmembers = 6
        while numbah < nmembers:
            rchoice = random.choice([x for x in guild.members])
            if rchoice not in rmembers:
                rmembers.append(rchoice)
                numbah += 1
        chosen = ', '.join([str(zzz) for zzz in rmembers])
        numbah = 0
        randint100 = 100
        em = discord.Embed(colour=0x36393f, description="**Dido2 VC Mode activated!!!1!**\nWorking\nInitializing protocol: **{}**\nLoading . . . done!".format(randprotocol))
        em.set_footer(text="Powered by Entropy | VC ANYONE?! | VC????? | VC!!!!!!1!!!!1!!!")
        em.add_field(name="Establishing communications", value=seq2[9].format(randint100), inline=False)
        em.add_field(name="Chosen targets can be found below.", value="Note that I'm not going to ping them, do that yourself", inline=False)
        while numbah < nmembers: 
            tarnum = numbah + 1
            em.add_field(name="Target #{}:".format(tarnum), value="**{}**".format(rmembers[numbah]), inline=True)
            await msg.edit(embed=em)
            numbah += 1
            await asyncio.sleep(random.randint(2, 4))
        await ctx.send("> gl in esports")

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

    @commands.group(autohelp=True)
    async def blindsociety(self, ctx):
        """Myeah"""
        pass

    @blindsociety.command()
    async def episodenames(self, ctx):
        thethings = {"1": "1) 14]",
                    "2": "[2) 5, 24]",
                    "3": "3) 3]",
                    "4": "[5) 7, 9]",
                    "5": "[6) 33, 40, 46",
                    "6": "9) 1, 18]",
                    "7": "[10) 32, 33][39",
                    "8": "11) 4, 12, 18]",
                    "9": "[12) 8, 9][17, 18]",
                    "10": "[13) 8, 9, 10][14, 17, 22",
                    "11": "14) 21, 30, 32",
                    "12": "15) 13, 20][22",
                    "13": "16) 20]",
                    "14": "[17) 6, 12",
                    "15": "20) 3, 4]",
                    "16": "There isn't actually step 16. The whole thing is:\n1) 14]\n[2) 5, 24] \n3) 3]\n[5) 7, 9]\n[6) 33, 40, 46\n9) 1, 18]\n[10) 32, 33][39\n11) 4, 12, 18]\n[12) 8, 9][17, 18]\n[13) 8, 9, 10][14, 17, 22\n14) 21, 30, 32\n15) 13, 20][22\n16) 20]\n[17) 6, 12\n20) 3, 4]\n\nI'm done for now. More clues if needed later."}
        em = discord.Embed(colour=0x36393f, description="**Okay, let me do my thing.**")
        em.set_footer(text=f"Still working... | {footer}")
        #times = 15
        thingy = await ctx.send(embed=em)
        for i in range(1, 17, 1):
            stuffs = str(i)
            em.add_field(name=f"Step {stuffs}:", value=f"**{thethings[stuffs]}**", inline=False)
            await asyncio.sleep(1)
            await thingy.edit(embed=em)
        em.description = "**Okay, I'm done.**"
        em.set_footer(text=f"Done. | {footer}")
        await thingy.edit(embed=em)

    @blindsociety.command()
    async def decipherepisodes(self, ctx):
        thethings = {
            "1": "The number in front of the right parenthesis is to indicate the episode number",
            "2": "The numbers afterwards are to show the letter number",
            "3": "The brackets indicate the end of words",
            "4": "Tourist Trapped: WELCOME TO GRAVITY FALLS\nGobblewonker: NEXT WEEK: RETURN TO BUTT ISLAND\nHeadhunters: HE’S STILL IN THE VENTS\nInconveniencing: ONWARDS AOSHIMA\nManliness: MR. CAESARIAN WILL BE OUT NEXT WEEK. MR. ATBASH WILL SUBSTITUTE\nTime Traveler: NOT H.G WELLS APPROVED\nFight Fighters: SORRY, DIPPER, BUT YOUR WENDY IS IN ANOTHER CASTLE\nLittle Dipper: THE INVISIBLE WIZARD IS WATCHING\nSummerween: BROUGHT TO YOU BY HOMEWORK: THE CANDY\nBoss Mabel: HEAVY IS THE HEAD THAT WEARS THE FEZ\nBottomless Pit!: NEXT UP: FOOTBOT TWO: GRUNKLE’S GREVENGE\nDeep End: VIVAN LOS PATOS DE LA PISCINA\nCarpet Diem: BUT WHO STOLE THE CAPERS\nBoyz Crazy: HAPPY NOW, ARIEL\nGideon Rises: SEARCH FOR THE BLINDEYE"
        }
        em = discord.Embed(colour=0x36393f, description="**Okay, let me do my thing.**")
        em.set_footer(text=f"Still working... | {footer}")
        thingy = await ctx.send(embed=em)
        for i in range(1, 5, 1):
            stuffs = str(i)
            if i <= 3:
                em.add_field(name=f"Step {stuffs}:", value=f"**{thethings[stuffs]}**", inline=False)
            if i == 4:
                em.add_field(name=f"Here's a list for convenience:", value=f"**{thethings[stuffs]}**", inline=False)
            await asyncio.sleep(0.5)
            await thingy.edit(embed=em)
        em.description = "**Okay, I'm done.**"
        em.set_footer(text=f"Done. | {footer}")
        await thingy.edit(embed=em)

    @blindsociety.command()
    async def solvedepisodes(self, ctx):
        answ = ("yes", "y", "ye", "yea", "yeah", "yesh", "sure", "yep", "da", "ok", "k", "okay")
        thethings = """*1) 14]*\n"Tourist Trapped: WELCOME TO GRAVITY FALLS" *is:*\n **I**
\n\n*[2) 5, 24]*\n"Gobblewonker: NEXT WEEK: RETURN TO BUTT ISLAND" *is:*\n **WA**
\n\n*3) 3]*\n"Headhunters: HE’S STILL IN THE VENTS" *is:*\n **S**
\n\n*[5) 7, 9]*\n"Inconveniencing: ONWARDS AOSHIMA" *is:*\n **SO**
\n\n*[6) 33, 40, 46*\n"Manliness: MR. CAESARIAN WILL BE OUT NEXT WEEK. MR. ATBASH WILL SUBSTITUTE" *is:*\n **BLI**
\n\n*9) 1, 18]*\n"Time Traveler: NOT H.G WELLS APPROVED" *is:*\n **ND**
\n\n*[10) 32, 33][39*\n"Fight Fighters: SORRY, DIPPER, BUT YOUR WENDY IS IN ANOTHER CASTLE" *is:*\n **HE L**
\n\n*11) 4, 12, 18]*\n"Little Dipper: THE INVISIBLE WIZARD IS WATCHING" *is:*\n **IED**
\n\n*[12) 8, 9][17, 18]*\n"Summerween: BROUGHT TO YOU BY HOMEWORK: THE CANDY" *is:*\n **TO ME**
\n\n*[13) 8, 9, 10][14, 17, 22*\n"Boss Mabel: HEAVY IS THE HEAD THAT WEARS THE FEZ" *is:*\n **THE DAR**
\n\n*14) 21, 30, 32*\n"Bottomless Pit!: NEXT UP: FOOTBOT TWO: GRUNKLE’S GREVENGE" *is:*\n **KNE**
\n\n*15) 13, 20][22*\n"Deep End: VIVAN LOS PATOS DE LA PISCINA" *is:*\n **SS I**
\n\n*16) 20]*\n"Carpet Diem: BUT WHO STOLE THE CAPERS" *is:*\n **S**
\n\n*[17) 6, 12*\n"Boyz Crazy: HAPPY NOW, ARIEL" *is:*\n **NE**
\n\n*20) 3, 4]*\n"Gideon Rises: SEARCH FOR THE BLINDEYE" *is:*\n **AR**"""
        em = discord.Embed(colour=0x36393f, description="**Are you sure you want to get the explanation to the thing? (answer with yes/no)**")
        em.set_footer(text=f"Waiting for reply | {footer}")
        thingy = await ctx.send(embed=em)
        def check(uh):
            return uh.author == ctx.author
        try:
            msg = await ctx.bot.wait_for("message", timeout=15.0, check=check)
            if msg.content.lower().strip() in answ:
                em.description = f"**Okay.**\n{thethings}"
                em.set_footer(text=f"Done. | {footer}")
            else:
                em.description = "**Welp, alrite.**"
                em.set_footer(text=f"Done. | {footer}")
        except asyncio.TimeoutError:
            em.description = "**Apparently not.**"
            em.set_footer(text=f"Done. | {footer}")
            await thingy.edit(embed=em)
        em.set_footer(text=f"Done. | {footer}")
        await thingy.edit(embed=em)
        await asyncio.sleep(10)
        await ctx.send(">>> So, the whole thing is:\n**I WAS SO BLIND HE LIED TO ME THE DARKNESS IS NEAR.**")
    
    @commands.command()
    async def thumbs(self, ctx, msg: int, channel: discord.TextChannel = None):
        if channel is None:
            chan = ctx.channel
        else:
            chan = channel
        message = await chan.fetch_message(msg)
        ru = message.reactions.users
        resp = await ru.users().flatten()
        #except AttributeError:
        #    resp = "> Well that failed. `(1)`"
        #    return await ctx.send(resp)
        #resp = f'>>> Users that reacted with:\n 👍\n{tup}.\n\nUsers that reacted with:\n 👎\n{tdown}.'
        await ctx.send(resp)