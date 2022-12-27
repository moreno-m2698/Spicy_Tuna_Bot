import os
import requests
import sys

riottoken = os.environ["RIOT_API_TOKEN"]

def getBinaryFromSummonerInfo(condensed_data: dict, key: str, condition, tfValues: tuple):
    if condensed_data == None:
        return None
    value = condensed_data[key]
    return tfValues[0] if value == condition else tfValues[1]

class PlayerDTO():
    def __init__(self, summoner_name: str, champion:str, kills: int, assists: int, deaths: int, gold: int, puuid: str, team_color, cs,win) -> None:
        self.summoner_name=summoner_name
        self.champion = champion
        self.kills = kills
        self.assists = assists
        self.deaths = deaths
        self.gold = gold
        self.puuid = puuid
        self.team_color = team_color
        self.kda = round((self.kills + self.assists) / 1, 2) if self.deaths == 0 else round((self.kills + self.assists) / self.deaths, 2)
        self.cs = cs
        self.win = win
    
    def __str__(self) -> str:
        return f'KDA: {self.kills}/{self.deaths}/{self.assists}  ({self.kda})'
    
class TeamDTO():
    def __init__(self,team: list) -> None:
        self.team = team
        self.team_color = getBinaryFromSummonerInfo(self.team[0], key ='teamId', condition = 100, tfValues = ('🟦','🟥'))
        self.player_list = []
        for player in self.team:
            self.player_list.append(PlayerDTO(player["summonerName"],player['championName'],player["kills"],\
                player["assists"], player["deaths"], player['goldEarned'], player["puuid"],self.team_color,player["totalMinionsKilled"]+player["neutralMinionsKilled"], player["win"]))

        self.win = getBinaryFromSummonerInfo(self.team[0], key='win', condition=True,tfValues=(True,False))
        self.team_gold = 0
        for player in self.team:
            self.team_gold += player['goldEarned']
    
    def winnerCrown(self) -> str:
        if self.win == True:
            return '👑'
        else:
            return ''


    def __str__(self) -> str:
        result = ''
        for player in self.team:
            result+=f'{player}\n'
        return result

class MatchDTO(): 
    def __init__(self,data:tuple, gamemode: str, duration, mainPlayer) -> None:
        self.data = data
        self.match = []
        for team in self.data:
            self.match.append(TeamDTO(team))
        self.gamemode = gamemode
        self.duration = duration
        self.min = int(self.duration/60)
        self.sec = self.duration%60
        self.mainPlayer = mainPlayer #Player of Focus    
    def __str__(self) -> str:
        result = ""
        for team in self.match:
            for player in team.player_list:
                result+=f'{player}\n'
            result+='\n'
        return result
    

    def createFieldsList(self)->list:
        result = []
        for team in self.match:
            result.append({"name": 
            f"{team.team_color}  Team Stats {team.winnerCrown()}",
            "value": f"🪙: {team.team_gold}g",
            "inline": "true"})
        for team in self.match:
            for player in team.player_list:
                result.append({"name": f"{player.team_color}  {player.summoner_name}: {player.champion}","value":f'{player} \
                    | gold: {player.gold}g | CS: {player.cs} | CS/min: {round(player.cs/(self.duration/60),1)}'})

        return result

    def MatchDTOToJSON(self)->dict:
        result = {
            "title": f"{self.mainPlayer.summoner_name}: {self.mainPlayer.champion}",
            "color": 11872010,
            "description": f"Gamemode: {self.gamemode} | Length:{self.min}min {self.sec}sec | CS: {self.mainPlayer.cs}",
            "thumbnail": {
                "url": f"https://ddragon.leagueoflegends.com/cdn/12.4.1/img/champion/{self.mainPlayer.champion}.png" #not full proof for certain champions so will go back and make more robust
                }, 
            "author": {
                "name":"Spicy Tuna",
                "url": "https://github.com/moreno-m2698/Spicy_Tuna_Bot",
                "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png"
                },
            "fields":self.createFieldsList()
                }
                

        return result


class RiotAPIWrapper():
    def __init__(self,token) -> None:
        self.token = token
    
    # Retrieves response from api using summoner name    
    def getSummonerInformation(self, name: str):
        base_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'

        try:
            url_name = name.replace(' ', '%20')
            access_url = f'{base_url}{url_name}?api_key={self.token}'
            response = requests.get(access_url).json()

            return response
        
        except:
            print('Either summoner name is incorrect or token is expired please speak to Becky at the front desk')
            return 

    # Uses player PUUID to create list of match ids
    def getMatchIDByPUUID(self, puuid:str, amount: int) -> list:
        matches_url =  'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'

        try:
            access_url = f'{matches_url}{puuid}/ids?start=0&count={amount}&api_key={self.token}'
            response = requests.get(access_url).json()
            return response
        
        except:
            print('invalid puuid or puuid accessed incorrect')

    # Converts match id to response holding match information
    def getMatch(self, match_id) -> dict:
        base_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/'

        try:
            access_url = f'{base_url}{match_id}?api_key={self.token}'
            response  = requests.get(access_url).json()
            return response

        except:
            print('Match ID not found')
            return

    def SummonerNametoMatchList(self,amount: int,name: str) -> list: # Gives list of 5v5 match IDs from summoner name
        puuid = self.getSummonerInformation(name)['puuid']
        match_id_list = self.getMatchIDByPUUID(puuid, amount)
        return match_id_list

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Methods for extracting information from api responses pertaining to game data which are then used to help in creating the embed interface   

        # Mapping function!!!!!!
    def getParticipantData(self, participant:dict) -> dict: #In theory will reduce the big partcipant dict into something we want
        wanted_keys = ["assists",'championName',"deaths","goldEarned","kills", "neutralMinionsKilled","puuid","summonerName","teamId","totalMinionsKilled","win"]
        information_dict = {}
        for key in wanted_keys:
            information_dict[key]=participant[key]
        return information_dict        

    # YOU NEED TO MAKE CASE FOR BOT GAMES: ONLY PRODUCES 5 PUUIDS AND THUS CAN NOT BE PROPERLY PASSED INTO THE DTO\

    def getMatchDTOFromMatchID(self, single_entry: str, summoner_name):
        gamejson = self.getMatch(single_entry)
        participants =gamejson["info"]["participants"]
        gamemode = gamejson["info"]["gameMode"]
        duration = gamejson["info"]["gameDuration"]
        puuid = self.getSummonerInformation(summoner_name)['puuid'] # Eventually find a way to just transfer along the function chain so we dont have to make seperate call
        playerindex = gamejson["metadata"]["participants"].index(puuid)
        mainPlayer = PlayerDTO(participants[playerindex]["summonerName"],participants[playerindex]['championName'],participants[playerindex]["kills"],\
            participants[playerindex]["assists"], participants[playerindex]["deaths"], participants[playerindex]['goldEarned'],
            participants[playerindex]["puuid"],participants[playerindex]["teamId"],
            participants[playerindex]["totalMinionsKilled"] + participants[playerindex]["neutralMinionsKilled"], participants[playerindex]["win"])
        desired_data = list(map(self.getParticipantData, participants))
        team1 = [summoner for summoner in desired_data if desired_data.index(summoner)<=4]
        team2 = [summoner for summoner in desired_data if desired_data.index(summoner)>4]
        teams  = (team1, team2)

        return MatchDTO(teams, gamemode, duration, mainPlayer)
    
    # Need match dto to process a list 

# [3:00 PM]
# - turrets taken
# [3:01 PM]
# - expand info - rune info
# [3:01 PM]
# expand info - items

wrapper = RiotAPIWrapper(riottoken)

