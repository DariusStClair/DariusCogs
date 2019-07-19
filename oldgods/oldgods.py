import discord
from redbot.core import commands
from random import choice, randint, random

randomwhisper = [
    ("Death is close..."),
    ("You are already dead"),
    ("Your courage will fail"),
    ("Your friends will abandon you"),
    ("You will betray your friends"),
    ("You will die"),
    ("You are weak"),
    ("Your heart will explode"),
    ("I am the lucid dream, the monster in your nightmares, the Fiend of a Thousand Faces, Cower before my true form! BOW DOWN BEFORE THE GOD OF DEATH!! MADNESS WILL CONSUME YOU!!"),
    ("They are coming for you..."),
    ("Give in to your fear..."),
    ("Kill them all... before they kill you..."),
    ("They have turned against you... now, take your revenge..."),
    ("It WAS your fault..."),
    ("Tell yourself again that these are not truly your friends..."),
    ("You are a pawn of forces unseen..."),
    ("There is no escape... not in this life... not in the next..."),
    ("Trust is your weakness..."),
    ("Hope is an illusion..."),
    ("All that you know will fade..."),
    ("You will be alone in the end..."),
    ("At the bottom of the ocean even light must die..."),
    ("The silent, sleeping, staring houses in the backwoods always dream... It would be merciful to tear them down..."),
    ("There is no sharp distinction between the real and the unreal..."),
    ("All places, all things have souls... All souls can be devoured..."),
    ("There is a little lamb lost in dark woods..."),
    ("The stars sweep chill currents that make men shiver in the dark..."),
    ("Do you dream while you sleep or is it an escape from the horrors of reality?"),
    ("Look around... They will all betray you... Flee screaming into the black forest..."),
    ("In the land of Ny'alotha there is only sleep..."),
    ("In the sleeping city of Ny'alotha walk only mad things..."),
    ("Ny'alotha is a city of old, terrible, unnumbered crimes..."),
    ("Y'knath k'th'rygg k'yi mrr'ungha gr'mula..."),
    ("The void sucks at your soul. It is content to feast slowly..."),
    ("The drowned god's heart is black ice..."),
    ("It is standing right behind you... Do not move... Do not breathe..."),
    ("Have you had the dream again? A black goat with seven eyes that watches from the outside..."),
    ("In the sunken city, he lays dreaming..."),
    ("Open me! Open me! Open me! Then only will you know peace"),
    ("Caress your fear"),
    ("Eyes are the windows to the soul... Shutter them forever"),
    ("When you walk among the black forest, you will see")
]
randomimg = [
    ("https://cdn.discordapp.com/attachments/583654519825760286/593625382528352276/unknown.png"),
    ("https://cdn.discordapp.com/attachments/583654519825760286/593625437490642944/unknown.png"),
    ("https://cdn.discordapp.com/attachments/583654519825760286/593625484311396363/unknown.png"),
    ("https://cdn.discordapp.com/attachments/583654519825760286/593625542528335882/unknown.png"),
    ("https://cdn.discordapp.com/attachments/583654519825760286/593625615652093957/unknown.png"),
    ("https://media-hearth.cursecdn.com/attachments/31/101/cthun-cutout.png"),
    ("https://cdn.discordapp.com/attachments/583654519825760286/593625903750316053/unknown.png")
]
etitle = "Shath'Yar"
edescr = "Those Who Sleep whisper to you"
efoot = "Shath'mag"
class Oldgods(commands.Cog):

    """Shadowy Whisperings"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["oldgodq", "quoteoldgod", "qoldgod"])
    async def oldgodquote(self, ctx):
        """
            Sends in a random quote from an Old God (Warcraft)
        """
        rwhisper = (choice(randomwhisper))
        rimg = (choice(randomimg))
        embed = discord.Embed()
        embed.colour = 15158332
        embed.title = etitle
        embed.description = edescr
        embed.set_thumbnail(url=rimg)
        embed.add_field(name=rwhisper, value=u'\u200b', inline=False)
        embed.set_footer(text=efoot)
        await ctx.send(embed=embed)