import os
import requests
import sys

riottoken = os.environ["RIOT_API_TOKEN"]

class PlayerDTO():
    def __init__(self, summoner_name: str, champion:str, kills: int, assists: int, deaths: int, gold: int, puuid: str) -> None:
        self.summoner_name=summoner_name
        self.champion = champion
        self.kills = kills
        self.assists = assists
        self.deaths = deaths
        self.gold = gold
        self.puuid = puuid
        self.kda = round((self.kills + self.assists) / 1, 2) if self.deaths == 0 else round((self.kills + self.assists) / self.deaths, 2)
    
    def __str__(self) -> str:
        return f'{self.summoner_name}: {self.champion} | KDA: {self.kills}/{self.deaths}/{self.assists}  ({self.kda})'
    
class TeamDTO():
    def __init__(self,team: list) -> None:
        self.team = team
        self.player_list = []
        for player in self.team:
            self.player_list.append(PlayerDTO(player["summonerName"],player['championName'],player["kills"],player["assists"], player["deaths"], player['goldEarned'], player["puuid"]))

    def __str__(self) -> str:
        result = ''
        for player in self.team:
            result+=f'{player}\n'
        return result

class MatchDTO(): 
    def __init__(self,data:tuple) -> None:
        self.data = data
        self.match = []
        for team in self.data:
            self.match.append(TeamDTO(team))
    
    def __str__(self) -> str:
        result = ""
        for team in self.match:
            for player in team.player_list:
                result+=f'{player}\n'
            result+='\n'
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
        print(match_id_list)
        
        result = []
        for game in match_id_list:
            result.append(self.getMatch(game))
            print(sys.getsizeof(self.getMatch(game)))
            
        return result

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Methods for extracting information from api responses pertaining to game data which are then used to help in creating the embed interface   

    # Create methods around accessing information thats relevant for player being used to access game information
    #   important: all player information
        # Mapping function!!!!!!
    def getParticipantData(self, participant:dict) -> dict: #In theory will reduce the big partcipant dict into something we want
        wanted_keys = ["assists",'championName',"deaths","goldEarned","kills","puuid","summonerName","teamId","win"]
        information_dict = {}
        for key in wanted_keys:
            information_dict[key]=participant[key]
        return information_dict

    def getMatchDTO(self, amount, summoner_name):
        all_game_data = self.SummonerNametoMatchList(amount, summoner_name)
        participants =all_game_data[0]["info"]["participants"] #Single element right now but will eventually have to think about loop implementation for a list of games
        desired_data = list(map(self.getParticipantData, participants))
        team1 = [summoner for summoner in desired_data if desired_data.index(summoner)<=4]
        team2 = [summoner for summoner in desired_data if desired_data.index(summoner)>4]
        teams  = (team1, team2)
        return MatchDTO(teams)

    def getBinaryFromSummonerInfo(condensed_data: dict, key: str, condition, tfValues: tuple):
        value = condensed_data[key]
        return tfValues[0] if value == condition else tfValues[1]

    def getPlayerGameStats(self, summoner_information):
        game_stats = {}
        game_stats['winlose'] = self.getBinaryFromSummonerInfo(summoner_information, key='win', condition=True,tfValues=('Win','Lose'))
        game_stats['teamcolor'] = self.getBinaryFromSummonerInfo(summoner_information, key ='teamId', condition = 100, tfValues = ('🟦','🟥'))
        return game_stats


# [3:00 PM]
# - enemy champs
# [3:00 PM]
# - ally champs
# [3:00 PM]
# - game length
# [3:00 PM]
# - turrets taken
# [3:01 PM]
# - expand info - rune info
# [3:01 PM]
# expand info - items

wrapper = RiotAPIWrapper(riottoken)

