import aiohttp
import asyncio
from math import floor, ceil
import datetime
import discord
from discord import utils
from redbot.core import checks, Config, bank, commands

class Leaguelib:
    def __init__(self, bot):
        self.url = "https://{}.api.riotgames.com"
        self.bot = bot
        self.api = None
        #"cache" things?
        self.champs = None
        self.freerotation = None
        self.champs_splash = None
        self.champs_ico = None
        self.champs_load = None
        #/"cache" things?
        self.cdragon = None
        self.imgs = None
        self._sess = aiohttp.ClientSession()
        self.srvs = {
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
            "pbe": "pbe1",
            "eun1": "eun1",
            "euw1": "euw1",
            "na1": "na1",
            "br1": "br1",
            "jp1": "jp1",
            "la1": "la1",
            "oc1": "oc1",
            "tr1": "tr1",
            "pbe1": "pbe1"
        }
        # Rito api / ddragon
        self.summ_name = "/lol/summoner/v4/summoners/by-name/{}"
        self.mastery_summ = "/lol/champion-mastery/v4/champion-masteries/by-summoner/{}"
        self.scores_summ = "/lol/champion-mastery/v4/scores/by-summoner/{}"
        self.mastery_summchamp = "/lol/champion-mastery/v4/champion-masteries/by-summoner/{}/by-champion/{}"
        self.positions_summid = "/lol/league/v4/positions/by-summoner/{}"
        self.active_summ = "/lol/spectator/v4/active-games/by-summoner/{}"
        self.match_matchid = "/lol/match/v4/matches/{}"
        self.matchlist_acc = "/lol/match/v4/matchlists/by-account/{}"
        self.ranked_test = "/lol/league/v4/entries/by-summoner/{}"
        self.shard_data = "/lol/status/v3/shard-data"
        self.rotations = "/lol/platform/v3/champion-rotations"
        # Community Dragon (cdragon)
        self.cdragon_champ = "https://cdn.communitydragon.org/{}/champion/"
        self.cdragon_champ_squareurl = "{}/square.png"
        self.cdragon_champ_dataurl = "{}/data"
    
    def cog_unload(self):
        self.__unload()

    async def __unload(self):
        asyncio.get_event_loop().create_task(self._sess.close())

    async def _getapi(self):
        if not self.api:
            db = await self.bot.db.api_tokens.get_raw("leaguehell", default=None)
            self.api = db["leagueapikey"]
            return self.api
        else:
            return self.api

    async def get_patch(self):
        ddragonv = "https://ddragon.leagueoflegends.com/api/versions.json"
        version = await self.get(ddragonv)
        return version[0]

    async def apistr(self):
        leagueapikey = await self._getapi()
        if leagueapikey is None:
            return False
        else:
            return "?api_key={}".format(leagueapikey)

    async def get(self, url):
        async with self._sess.get(url) as r:
            return await r.json()

    async def get_puuid(self, name, xreg):
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.summ_name.format(name) + apistr
        rj = await self.get(rq)
        return rj["puuid"]

    async def get_aid(self, name, xreg):
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.summ_name.format(name) + apistr
        rj = await self.get(rq)
        return rj["accountId"]

    async def get_sid(self, name, xreg):
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.summ_name.format(name) + apistr
        rj = await self.get(rq)
        return rj["id"]
        #return rj["id"]

    async def get_prname(self, name, xreg):
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.summ_name.format(name) + apistr
        rj = await self.get(rq)
        return rj["name"]
    
    async def get_champ_masteries(self, name, xreg):
        summid = await self.get_sid(name, xreg)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.mastery_summ.format(summid) + apistr
        rj = await self.get(rq)
        return rj

    async def get_champ_name(self, champid):
        if self.champs is None:
            await self.upd_champs()
        champ = self.champs["data"]
        if champid == -1:
            return "Wut"
        for i in champ:
            if champ[i]["key"] == champid:
                return champ[i]["name"]

    async def get_mastery(self, name, xreg):
        summid = await self.get_sid(name, xreg)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.scores_summ.format(summid) + apistr
        rj = await self.get(rq)
        return rj

    async def get_champ_title(self, champid):
        if self.champs is None:
            await self.upd_champs()
        champ = self.champs["data"]
        if champid == -1:
            return "Wut"
        for i in champ:
            if champ[i]["key"] == champid:
                return champ[i]["title"]

    async def upd_champs(self):
        #ddragonv = "https://ddragon.leagueoflegends.com/api/versions.json"
        version = await self.get_patch()
        rq = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
        self.champs = await self.get(rq)

    async def upd_champ_rotation(self):
        apistr = await self.apistr()
        xreg = "eune"
        rq = self.url.format(self.srvs[xreg]) + self.rotations + apistr
        self.freerotation = await self.get(rq)

    async def champ_rotation(self):
        if self.freerotation is None:
            await self.upd_champ_rotation()
        rotation = self.freerotation["freeChampionIds"]
        #for i in rotation:
        #    chname = await self.get_champ_name()
        return rotation

    async def ddragon_icon(self, pid):
        #ddragonv = "https://ddragon.leagueoflegends.com/api/versions.json"
        version = await self.get_patch()
        iconid = pid
        rq = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{iconid}.png"
        return rq

    async def ddragon_champico(self, champid):
        #ddragonv = "https://ddragon.leagueoflegends.com/api/versions.json"
        version = await self.get_patch()
        chnametemp = str(await self.get_champ_name(champid))
        temp = await self.champ_sanitize_name(chnametemp)
        rq = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{temp}.png"
        return rq

    # Community dragon champstuff
    async def cdragon_champ_square(self, champname):
        champkey = await self.get_champid(champname)
        if champkey != "Invalid champ":
            version = await self.get_patch()
            #self.url.format(self.srvs[xreg]) + self.mastery_summchamp.format(summid, champid)
            square = self.cdragon_champ.format(version) + self.cdragon_champ_squareurl.format(champkey)
            return square
        else:
            version = await self.get_patch()
            return f"https://cdn.communitydragon.org/{version}/champion/generic/square.png"

    async def cdragon_champ_data(self, champname):
        champkey = await self.get_champid(champname)
        if champkey != "Invalid champ":
            version = await self.get_patch()
            cdchampdata = self.cdragon_champ.format(version) + self.cdragon_champ_dataurl.format(champkey)
            rj = await self.get(cdchampdata)
            return rj
        else:
            return "Error"

    async def ddragon_champsplash(self, champid):
        #ddragonv = "https://ddragon.leagueoflegends.com/api/versions.json"
        #version = await self.get(ddragonv)
        chnametemp = str(await self.get_champ_name(champid))
        temp = await self.champ_sanitize_name(chnametemp)
        #rq = f"http://ddragon.leagueoflegends.com/cdn/{version[0]}/img/champion/splash/{splashid}_0.jpg"
        rq = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{temp}_0.jpg"
        return rq

    async def ddragon_champsloading(self, champid):
        #ddragonv = "https://ddragon.leagueoflegends.com/api/versions.json"
        #version = await self.get(ddragonv)
        chnametemp = str(await self.get_champ_name(champid))
        temp = await self.champ_sanitize_name(chnametemp)
        #rq = f"http://ddragon.leagueoflegends.com/cdn/{version[0]}/img/champion/splash/{splashid}_0.jpg"
        rq = f"http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{temp}_0.jpg"
        return rq

    async def champ_name_sanitized(self, champid):
        chnametemp = str(await self.get_champ_name(champid))
        chnametempr = str(chnametemp.replace("'", ""))
        temp = chnametempr.capitalize()
        if temp == "Reksai":
            temp = "RekSai"
        if temp == "Jarvan iv":
            temp = "JarvanIV"
        if temp == "Master yi":
            temp = "MasterYi"
        if temp == "Miss fortune":
            temp = "MissFortune"
        if temp == "Kogmaw":
            temp = "KogMaw"
        if temp == "Lee sin":
            temp = "LeeSin"
        if temp == "Nunu & willump":
            temp = "Nunu"
        if temp == "Leblanc":
            temp = "LeBlanc"
        if temp == "Tahm kench":
            temp = "TahmKench"
        if temp == "Khazix":
            temp = "KhaZix"
        if temp == "Xin zhao":
            temp = "XinZhao"
        if temp == "Wukong":
            temp = "MonkeyKing"
        return temp

    async def champ_sanitize_name(self, chnametemp):
        chnametemp = str(chnametemp.replace("'", ""))
        temp = chnametemp.capitalize()
        if temp == "Reksai":
            temp = "RekSai"
        if temp == "Jarvan iv":
            temp = "JarvanIV"
        if temp == "Master yi":
            temp = "MasterYi"
        if temp == "Miss fortune":
            temp = "MissFortune"
        if temp == "Kogmaw":
            temp = "KogMaw"
        if temp == "Lee sin":
            temp = "LeeSin"
        if temp == "Nunu & willump":
            temp = "Nunu"
        if temp == "Leblanc":
            temp = "LeBlanc"
        if temp == "Tahm kench":
            temp = "TahmKench"
        if temp == "Khazix":
            temp = "KhaZix"
        if temp == "Xin zhao":
            temp = "XinZhao"
        if temp == "Wukong":
            temp = "MonkeyKing"
        return temp

    async def summ_icon(self, name, xreg):
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.summ_name.format(name) + apistr
        rj = await self.get(rq)
        pid = rj["profileIconId"]
        iconimg = await self.ddragon_icon(pid)
        return iconimg

    async def get_champlist(self):
        if self.champs is None:
            await self.upd_champs()
        champ = self.champs["data"]
        #for i in champ:
        #    if champ[i]["name"].lower == str(name).lower:
        #        return champ[i]["key"]
        return champ
        #return "> Welp, that's an error"
        
    async def get_champ_data(self, name):
        if self.champs is None:
            await self.upd_champs()
        champ = await self.get_champid(name)
        data = self.get_champlist
        resp = data[champ]
        return resp

    async def get_champid(self, name):
        clist = await self.get_champlist()
        searched = str(name)
        if " " not in searched:
            searched = str(name)
        else:
            searched = "".join(searched.split(" "))
        if "'" in searched:
            searched = "".join(searched.split("'"))
        if "." in searched:
            searched = "".join(searched.split("."))
        if "&" in searched:
            searched = "".join(searched.split("&"))
        for i in clist:
            temp = str(clist[i]["id"])
            if temp.lower() == searched.lower():
                return clist[i]["key"]
        return "Invalid champ"

    async def get_champ_mastery(self, name, xreg, champid):
        summid = await self.get_sid(name, xreg)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.mastery_summchamp.format(summid, champid) + apistr
        rj = await self.get(rq)
        res = {}
        res["mastery"] = rj["championLevel"]
        res["points"] = rj["championPoints"]
        return res
        #return rj

    async def get_elo(self, name, xreg):
        summid = await self.get_sid(name, xreg)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.positions_summid.format(summid) + apistr
        rj = await self.get(rq)
        return rj
        #if rj != []:
        #    dct = rj[0]
        #    res = dct["tier"] + " " + dct["rank"] + " " + str(dct["leaguepoints"]) + " LP"
        #else:
        #    res = "Unranked"
        #return res
    
    async def game_info(self, name, xreg):
        summid = await self.get_sid(name, xreg)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.active_summ.format(summid) + apistr
        rj = await self.get(rq)
        if rj["gameMode"] == "CLASSIC":
            if rj["gameType"] == "MATCHED_GAME":
                gamemode = "Ranked 5vs5"
            else:
                gamemode = "Normal 5vs5"

        else:
            gamemode = " ".join([rj["gameMode"], rj["gameType"]])
        res = {}
        res["gamemode"] = "{} is currently playing {}".format(name, gamemode)
        res["team1"] = {}
        res["team2"] = {}
        res["team1"]["bans"] = {}
        res["team2"]["bans"] = {}
        res["team1"]["players"] = {}
        res["team2"]["players"] = {}
        for i in rj["bannedChampions"]:
            name = await self.get_champ_name(str(i["championId"]))
            if name is None:
                name = "No ban"
            if i["teamId"] == 100:
                res["team1"]["bans"][name] = i["pickTurn"]
            else:
                res["team2"]["bans"][name] = i["pickTurn"]
        for i in rj["participants"]:
            sumname = i["summonerName"]
            champ = await self.get_champ_name(str(i["championId"]))
            name = sumname + ": " + champ
            elo = await self.get_elo(xreg, sumname)
            if i["teamId"] == 100:
                res["team1"]["players"][name] = elo
            else:
                res["team2"]["players"][name] = elo
        return res

    async def get_match(self, xreg, matchid):
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.match_matchid.format(matchid) + apistr
        rj = await self.get(rq)
        return rj
        
    async def get_history(self, name, xreg):
        summid = await self.get_aid(name, xreg)
        cpt = 5
        if not summid:
            return False
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.matchlist_acc.format(summid) + apistr
        rj = await self.get(rq)
        clean = {}
        count = 0
        for i in rj["matches"]:
            temp = {}
            temp["champ"] = await self.get_champ_name(str(i["champion"]))
            temp["role"] = i["lane"]
            if temp["role"].lower() == "none":
                temp["role"] = i["role"]
            match = await self.get_match(xreg, i["gameId"])
            osf = floor((match["gameDuration"])/60)
            temp["Duration"] = str(osf) + ":" + str(match["gameDuration"] - (osf*60))
            temp["Gamemode"] = match["gameMode"]
            ts = i["timestamp"] /1000
            temp["hour"] = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
            achampid = i["champion"]
            for k in match["participants"]:
                if k["championId"] == achampid:
                    tempvar = k
                    team = k["teamId"]
                    break
            for p in match["teams"]:
                if p["teamId"] == team:
                    reslt = p["win"]
                    break
            if reslt == "win":
                temp["result"] = reslt
            else:
                temp["result"] = "loss"
            stat = tempvar["stats"]
            temp["kda"] = str(stat["kills"]) + " kills / " + str(stat["deaths"]) + " deaths / " + str(stat["assists"]) + " assists."
            temp["gold"] = str(stat["goldEarned"]) + " gold earned."
            clean[count] = temp
            count += 1
            if count == cpt:
                return clean
            await asyncio.sleep(0.5)
        return clean

    async def get_ranked(self, name, xreg):
        summid = await self.get_sid(name, xreg)
        if not summid:
            return False
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + self.ranked_test.format(summid) + apistr
        rj = await self.get(rq)
        for i in rj:
            if i["queueType"] == "RANKED_SOLO_5x5":
                i["queueType"] = "Solo/duo"
            if i["queueType"] == "RANKED_TEAM_5x5":
                i["queueType"] = "Team 5vs5"
            if i["queueType"] == "RANKED_TEAM_3x3":
                i["queueType"] = "Team 3vs3"
            if i["queueType"] == "RANKED_TFT":
                i["queueType"] = "Teamfight Tactics"
            if i["queueType"] == "RANKED_FLEX_SR":
                i["queueType"] = "Flex 5vs5"
            if i["queueType"] == "RANKED_FLEX_TT":
                i["queueType"] = "Flex 3vs3"
        return rj

    async def ranked_q(self, uhelo):
        rankeds =	{
        "RANKED_SOLO_5x5": "Solo/duo",
        "RANKED_TEAM_5x5": "Flex",
        "RANKED_TEAM_3x3": "3vs3"
        }
        try:
            qtype = uhelo[rankeds["queueType"]]
        except KeyError:
            return "Shit happened"
        return qtype

    async def champ_emoji(self, chid):
        emoji = "<:None:612702016094863518>"
        for n_ in self.bot.emojis:
            if n_.name == chid:
                emoji = f"<:{n_.name}:{n_.id}>"
        return emoji

    async def statusdata(self, xreg):
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return None
        rq = self.url.format(self.srvs[xreg]) + self.shard_data + apistr
        rj = await self.get(rq)
        return rj
