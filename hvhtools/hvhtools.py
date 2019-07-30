# Discord
import discord
# Red
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
        emen.set_footer(text=footer)
        await ctx.send(emen)

    @hvh.command()
    async def rulesru(self, ctx):
        """Embeds the rules in: **Russian**"""
        await ctx.send('Test ru')

    @hvh.command()
    async def rulesbg(self, ctx):
        """Embeds the rules in: **Bulgarian**"""
        await ctx.send('Test bg')
