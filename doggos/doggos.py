# Post animal pics by Eslyium#1949 & Yukirin#0048 is the original thingy
# I'm just using it for golden retrievers because of Lyutenitsa

# Discord
import discord

# Red
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, box, inline

# Libs
import aiohttp

goldenapi = "https://dog.ceo/api/breed/retriever/golden/images/random"
shepherdapi = "https://dog.ceo/api/breed/germanshepherd/images/random"
huskyapi = "https://dog.ceo/api/breed/husky/images/random"
coonapi = "https://api.thecatapi.com/v1/images/search?breed_ids=mcoo"

BaseCog = getattr(commands, "Cog", object)
emtitleretriever = "Here, have the goodest doggo"
emtitleshepherd = "Bork bork something"
emtitlehusky = "Where's Moon Moon"
emtitlecoon = "Was it so hard to get here?"
emcolor = 15158332

class Doggos(BaseCog):
    """Posts Golden retrievers and German Shepherds!"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
        self.goldenapi = goldenapi
        self.shepherdapi = shepherdapi
        self.huskyapi = huskyapi
        self.coonapi = coonapi

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def goldendoggo(self, ctx):
        """Shows a random golden retriever photo"""
        async with self.session.get(self.goldenapi) as r:
            result = await r.json()
        emimg = str(result['message'])
        embed = discord.Embed(title=emtitleretriever)
        embed.url = emimg
        embed.colour = emcolor
        embed.set_image(url=emimg)
        embed.description = bold(("[Click to view it in your browser]({url})")).format(url=emimg)
        embed.set_footer(text="               Hell's Doggos are powered by dog.ceo, also Dido2 really wanted this")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def goldendoggos(self, ctx, amount : int = 5):
        """Throws a golden retriever bomb!
        Defaults to 5, max is 10 (thanks Eslyium#1949 & Yukirin#0048)"""
        results = []
        if amount > 10 or amount < 1:
            amount = 5
        try:
            for x in range(0,amount):
                async with self.session.get(self.goldenapi) as r:
                    api_result = await r.json()
                    results.append(api_result['message'])
            await ctx.send("\n".join(results))
        except:
            await ctx.send("API Error")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def gshepherd(self, ctx):
        """Shows a random german shepherd photo"""
        async with self.session.get(self.shepherdapi) as r:
            result = await r.json()
        emimg = str(result['message'])
        embed = discord.Embed(title=emtitleshepherd)
        embed.url = emimg
        embed.colour = emcolor
        embed.set_image(url=emimg)
        embed.description = bold(("[Click to view it in your browser]({url})")).format(url=emimg)
        embed.set_footer(text="               Hell's Doggos are powered by dog.ceo, dedicated to Velven")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def gshepherds(self, ctx, amount : int = 5):
        """Throws a german shepherds bomb!
        Defaults to 5, max is 10 (thanks Eslyium#1949 & Yukirin#0048)"""
        results = []
        if amount > 10 or amount < 1:
            amount = 5
        try:
            for x in range(0,amount):
                async with self.session.get(self.shepherdapi) as r:
                    api_result = await r.json()
                    results.append(api_result['message'])
            await ctx.send("\n".join(results))
        except:
            await ctx.send("API Error")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def husky(self, ctx):
        """Shows a random husky photo"""
        async with self.session.get(self.huskyapi) as r:
            result = await r.json()
        emimg = str(result['message'])
        embed = discord.Embed(title=emtitlehusky)
        embed.url = emimg
        embed.colour = emcolor
        embed.set_image(url=emimg)
        embed.description = bold(("[Click to view it in your browser]({url})")).format(url=emimg)
        embed.set_footer(text="               Hell's Doggos are powered by dog.ceo, mozuk Chris")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def coon(self, ctx):
        """Shows a random maine coon photo"""
        async with self.session.get(self.coonapi) as r:
            result = await r.json()
        emimg = str(result[0]["breeds"][0]['url'])
        embed = discord.Embed(title=emtitlecoon)
        embed.url = emimg
        embed.colour = emcolor
        embed.set_image(url=emimg)
        embed.description = bold(("[Click to view it in your browser]({url})")).format(url=emimg)
        embed.set_footer(text="               Hell's Mialos are powered by thecatapi.com, gj Caine Moon")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def huskies(self, ctx, amount : int = 5):
        """Throws a husky bomb!
        Defaults to 5, max is 10 (thanks Eslyium#1949 & Yukirin#0048)"""
        results = []
        if amount > 10 or amount < 1:
            amount = 5
        try:
            for x in range(0,amount):
                async with self.session.get(self.huskyapi) as r:
                    api_result = await r.json()
                    results.append(api_result['message'])
            await ctx.send("\n".join(results))
        except:
            await ctx.send("API Error")
            
    def __unload(self):
        self.bot.loop.create_task(self.session.close())
