import os
import requests
import sys

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
            print(sys.getsizeof(self.getMatchList(game)))
            
        return result

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #Methods for extracting information from api responses pertaining to game data which are then used to help in creating the embed interface   
     
    def getPUUIDGameMetadataFromSummonerName(self,game_list: list):
        response = game_list[0]
        metadata_puuid_list = response["metadata"]["participants"]
        return metadata_puuid_list

    # THINK ABOUT TRYING TO MAKE A 2 ELEMENT LIST TO HOLD THE INFORMATION SO THAT WE DO NOT HAVE  TO CALL TWICE

    def getGameInformationFromSummonerName(self, game_list:list):
        response = game_list[0]
        game_information_list = response["info"]["participants"]
        return game_information_list

    def getSummonerGameInformation(self, game_list: list, summoner_name: str):
        game_information = self.getGameInformationFromSummonerName(game_list)
        puuid_metadata = self.getPUUIDGameMetadataFromSummonerName(game_list)
        summoner_index = puuid_metadata.index(self.getSummonerInformation(summoner_name)['puuid'])
        summoner_information = game_information[summoner_index]
        return summoner_information

    def getPlayerChampionName(self, summoner_information):
        champion_name = summoner_information["championName"]
        return f'{summoner_information["summonerName"]}: {champion_name}'

    def getPlayerKDA(self, summoner_information): # Add case for perfect game
        player_kills = summoner_information["kills"]
        player_deaths = summoner_information["deaths"]
        player_assists = summoner_information["assists"]
        kda = f'{round((player_kills + player_assists) / player_deaths, 2)}:1'
        return f'KDA: {kda}'

    def getPlayerGold(self, summoner_information):
        gold_earned = summoner_information["goldEarned"]
        return f'Gold Earned: {gold_earned}'

    def getGamemode(self,summoner_name):
        information = self.SummonertoMatchList(1, summoner_name)[0]
        gamemode = information['info']['gameMode']
        return f'Gamemode: {gamemode}'

    def getWinLose(self, summoner_information):
        conclusion = summoner_information["win"]
        if conclusion == True:
            return f'Game win'
        else:
            return f'Game Lose'

    def getTeamColor(self, summoner_information):
        team_color = summoner_information["teamId"]
        if team_color == 100:
            return '🟦'
        else:
            return '🟥'     

    def organizePlayerstoTeams(self, summoner_name):
        game_information = self.getGameInformationFromSummonerName(self.SummonertoMatchList(1, summoner_name))
        team1 = [summoner['summonerName'] for summoner in game_information if game_information.index(summoner)<=4]
        team2 = [summoner['summonerName'] for summoner in game_information if game_information.index(summoner)>4]
        teams = (team1, team2)
        return f'{teams}'


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

