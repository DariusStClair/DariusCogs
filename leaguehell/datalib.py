import discord
from discord import utils

class Datalib:
    def __init__(self, bot):
        self.bot = bot
        self.SERVERS = {
            "eune": "eun1",
            "euw": "euw1",
            "na": "na1",
            "br": "br1",
            "jp": "jp1",
            "kr": "kr",
            "lan": "la1",
            "oce": "oc1",
            "tr": "tr1",
            "ru": "ru",
            "pbe1": "pbe1",
            "eune1": "eun1",
            "euw1": "euw1",
            "na1": "na1",
            "br1": "br1",
            "jp1": "jp1",
            "la1": "la1",
            "oc1": "oc1",
            "tr1": "tr1",
            "pbe1": "pbe1"
        }
        
        self.OPGGSERVERS = {
            "eun1": "eune",
            "euw1": "euw",
            "na1": "na",
            "br1": "br",
            "jp1": "jp",
            "kr": "kr",
            "la1": "lan",
            "oc1": "oce",
            "tr1": "tr",
            "ru": "ru",
            "pbe1": "pbe",
            "eune": "eune",
            "euw": "euw",
            "na": "na",
            "br": "br",
            "jp": "jp",
            "la": "lan",
            "oce": "oc",
            "tr": "tr",
            "pbe": "pbe"
        }

        self.GAMETYPES = {
            "CUSTOM_GAME": "Custom Game",
            "TUTORIAL_GAME": "Tutorial Game",
            "MATCHED_GAME": "Matched Game"
        }

        self.GAMEMODES = {
            "CLASSIC": "Classic",
            "ODIN": "Crystal Scar",
            "ARAM": "ARAM",
            "TUTORIAL": "Tutorial",
            "URF": "Ultra Rapid Fire!!1!11!",
            "DOOMBOTSTEEMO": "Doom Bots",
            "ONEFORALL": "One for All",
            "ASCENSION": "Ascension",
            "FIRSTBLOOD": "Snowdown Showdown",
            "KINGPORO": "Legends of the Poro King",
            "SIGE": "Nexus Siege",
            "ASSASSINATE": "Blood Hunt",
            "ARSR": "All Random Summoner's Rift",
            "DARKSTAR": "Dark Star: Singularity",
            "STARGUARDIAN": "Star Guardian Invasion",
            "PROJECT": "PROJECT: Hunters",
            "GAMMODEX": "Nexus Blitz",
            "ODYSSEY": "Odyssey: Extraction"
        }