import os
import requests

riottoken = os.environ["RIOT_API_TOKEN"]

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
    def getMatchList(self, match_id):
        base_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/'

        try:
            access_url = f'{base_url}{match_id}?api_key={self.token}'
            response  = requests.get(access_url).json()
            return response

        except:
            print('Match ID not found')
            return

    # Melds methods together
    def SummonertoMatchList(self,amount: int,name: str) -> list: 
        puuid = self.getSummonerInformation(name)['puuid']
        match_id_list = self.getMatchIDByPUUID(puuid, amount)
        print(match_id_list)
        
        result = []
        for game in match_id_list:
            result.append(self.getMatchList(game))
        
        
        return result

# !lolmatch Umbrall 3
# [2:59 PM]
# !lolmatch Umbrall
# [3:00 PM]
# - Summoner champion
# [3:00 PM]
# - kda
# [3:00 PM]
# - total gold
# [3:00 PM]
# - game mode
# [3:00 PM]
# - enemy champs
# [3:00 PM]
# - ally champs
# [3:00 PM]
# - game length
# [3:00 PM]
# - turrets taken
# [3:00 PM]
# - win/lose
# [3:01 PM]
# - expand info - rune info
# [3:01 PM]
# expand info - items

wrapper = RiotAPIWrapper(riottoken)

