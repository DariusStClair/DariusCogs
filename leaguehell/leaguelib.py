import aiohttp
import asyncio
from math import floor, ceil
import datetime

class Leaguelib:
    def __init__(self, bot):
        self.url = "https://{}.api.riotgames.com"
        self.bot = bot
        self.api = None
        self.champs = None
        self._sess = aiohttp.ClientSession()
        self.srvs = {
            "eune": "eun1",
            "euw": "euw1",
            "na": "na1"
        }

    async def __unload(self):
        self._sess.detach()

    async def _getapi(self):
        if not self.api:
            db = await self.bot.db.api_tokens.get_raw("leaguehell", default=None)
            self.api = db["leagueapikey"]
            return self.api
        else:
            return self.api

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
        rq = self.url.format(self.srvs[xreg]) + "/lol/summoner/v4/summoners/by-name/{}".format(name) + apistr()
        rj = await self.get(rq)
        return rj["puuid"]

    async def get_aid(self, name, xreg):
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + "/lol/summoner/v4/summoners/by-name/{}".format(name) + apistr()
        rj = await self.get(rq)
        return rj["accountId"]

    async def get_sid(self, name, xreg):
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + "/lol/summoner/v4/summoners/by-name/{}".format(name) + apistr()
        rj = await self.get(rq)
        return rj["id"]
    
    async def get_champ_masteries(self, name, xreg):
        summid = await self.get_sid(xreg, name)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + "/lol/summoner/v4/summoners/champion-masteries/by-summoner/{}".format(summid) + apistr()
        rj = await self.get(rq)
        return rj

    async def get_mastery(self, name, xreg):
        summid = await self.get_sid(xreg, name)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + "/lol/summoner/v4/summoners/scores/by-summoner/{}".format(summid) + apistr()
        rj = await self.get(rq)
        return rj

    async def get_champ_name(self, champid):
        if self.champs is None:
            await self.upd_champs()
        champ = self.champs["data"]
        if idchamp == -1:
            return "Wut"
        for i in champ:
            if champ[i]["key"] == idchamp:
                return champ[i]["name"]

    async def upd_champs(self):
        ddragonv = "https://ddragon.leagueoflegends.com/api/versions.json"
        version = await self.get(ddragonv)
        rq = f"http://ddragon.leagueoflegends.com/cdn/{version[0]}/data/en_US/champion.json"
        self.champs = await self.get(rq)

    async def get_champid(self, *name):
        if self.champs is None:
            await self.upd_champs()
        champ = self.champs["data"]
        for i in champ:
            if champ[i]["name"] == name:
                return champ[i]["key"]
        return "Wtf champ we"

    async def get_champ_mastery(self, name, xreg, idchamp):
        summid = await self.get_sid(xreg, name)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + "/lol/champion-mastery/v4/champion-masteries/by-summoner/{}/by-champion/{}".format(summid, champid) + apistr
        rj = await self.get(rq)
        res = {}
        res["mastery"] = rj["championLevel"]
        res["points"] = rj["championPoints"]
        return res

    async def get_elo(self, name, xreg):
        summid = await self.get_sid(xreg, name)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + "/lol/league/v4/positions/by-summoner/{}".format(summid) + apistr
        rj = await self.get(rq)
        if rj != []:
            dct = js[0]
            res = dct["tier"] + " " + dct["rank"] + " " + str(dct["leaguepoints"]) + " LP"
        else:
            res = "Unranked"
        return res
    
    async def game_info(self, name, xreg):
        summid = await self.get_sid(xreg, name)
        apistr = await self.apistr()
        if xreg not in self.srvs:
            return False
        rq = self.url.format(self.srvs[xreg]) + "/lol/spectator/v4/active-games/by-summoner/{}".format(summid) + apistr
        rj = await self.get(rq)
        if rj["gameMode"] == "CLASSIC":
            if rj["gameType"] == "MATCHED_GAME":
                gamemode = "Ranked 5vs5"
            else:
                gamemode = "Normal 5vs5"

        else:
            gamemode = " ".join([js["gameMode"], js["gameType"]])
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
            rq = self.url.format(self.srvs[xreg]) + "/lol/match/v4/matches/{}".format(matchid) + apistr
            rj = await self.get(rq)
            return rj
        
        async def get_history(self, cpt, name, xreg):
            summid = await self.get_aid(xreg, name)
            if not summid:
                return False
            apistr = await self.apistr()
            if xreg not in self.srvs:
                return False
            rq = self.url.format(self.srvs[xreg]) + "/lol/match/v4/matchlists/by-account/{}".format(sumid) + apistr
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
                champid = i["champion"]
                for k in match["participants"]:
                    if k["championId"] == champid:
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