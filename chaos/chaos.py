# Discord
import discord
# Red
from discord import Message, message
from redbot.core import checks, Config, commands
from redbot.core.utils.chat_formatting import bold, box, inline
# Libs

footer = "Powered by Entropy"

class Chaos(commands.Cog):
    """I'll write down something here... someday."""

    def __init__(self, bot):
        self.bot = bot