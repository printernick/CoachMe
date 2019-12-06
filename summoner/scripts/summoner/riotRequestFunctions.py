import requests

def requestSummonerData(region: str, summonerName: str, APIKey: str):
    '''
    region: RU, KR, BR1, OC1, JP1, NA1, EUN1, EUW1, TR1, LA1, LA2

    '''
    URL = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={APIKey}"
    response = requests.get(URL)
    return response.json()

# def requestEntriesBySummoner(region:str, encryptedSummonerId: str, APIKey: str):
#     # URL = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={APIKey}"
#     URL = "adsf"
#     response = requests.get(URL)
#     return response.json()

def requestMatchlist(region: str, encryptedAccountId: str, APIKey: str):
    '''
    region: RU, KR, BR1, OC1, JP1, NA1, EUN1, EUW1, TR1, LA1, LA2

    '''

    URL = f"https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{encryptedAccountId}?api_key={APIKey}"
    response = requests.get(URL)
    return response.json()