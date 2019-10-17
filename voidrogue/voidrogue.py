# Discord
import discord
# Red
from discord import Message, message
from redbot.core import checks, Config, commands
from redbot.core.utils.chat_formatting import bold, box, inline
# Libs

footer = "Powered by Entropy"

class Voidrogue(commands.Cog):
    """I'll write down something here... someday."""

    def __init__(self, bot):
        self.bot = bot
        self._movecontrols = ["⬆️", "⬇️", "⬅️", "➡️"]
        self._movectrl = {
            "up": "⬆️",
            "down": "⬇️",
            "left": "⬅️",
            "right": "➡️"
        }
        default_global = {
            "active": False,
            "psizemax": 3
        }
        default_user = {
            "Name": None,
        }
        default_guild = {
            "db": [],
            "achannel": None,
            "pos": None,
            "mvmnt": None,
            "actions": None,
            "party": None,
            "psize": 0,
            "pleader": None
        }
        self.config = Config.get_conf(self, identifier=690112666, force_registration=True)
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
        self.config.register_user(**default_user)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def ctest(self, ctx):
        author = ctx.author
        channel = ctx.channel