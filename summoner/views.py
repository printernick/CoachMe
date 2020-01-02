from django.shortcuts import render
import logging
import os

from .scripts.summoner import riotRequestFunctions as riot
from riotwatcher import RiotWatcher, ApiError

def home(request):
    summoner_name = request.GET.get('summoner_name')
    region = request.GET.get("region")

    # Get Api key
    cur_path = os.getcwd()
    file = open(os.path.join(cur_path, '_info', 'api.txt'), "r") #path to api key
    APIKey = file.read()

    watcher = RiotWatcher(APIKey)
    try:
        summoner_data = watcher.summoner.by_name(region, summoner_name)
    except ApiError as e:
        status_code = e.response.status_code
        return render(request, "summoner/error.html", {"summonerData": {"name": summoner_name}, "status": status_code})

    # if summoner not found
    if "status" in summoner_data:
        return render(request, "summoner/error.html", {"summonerData": {"name": summoner_name}})

    match_list = watcher.match.matchlist_by_account(region, summoner_data["accountId"], end_index=25)['matches']
    matches = {}
    champion_ids = {}
    for match in match_list[:min(25, len(match_list))]:
        match_by_id = watcher.match.by_id(region, match["gameId"])

        # 0th index = blue team, 1st index = red team
        for ban in zip(match_by_id['teams'][0]['bans'], match_by_id['teams'][1]['bans']):
            for i in range(len(ban)):
                id = str(ban[i]['championId'])
                if id not in champion_ids:
                    champion_json = riot.getStaticChampionInfo(id)
                    champion_ids[id] = champion_json

    league_data = watcher.league.by_summoner(region, summoner_data["id"])

    #Static content
    version = watcher.data_dragon.versions_for_region(region)['v']
    champions = watcher.data_dragon.champions(version)['data']
    items = watcher.data_dragon.items(version)['data']
    profile_icons = watcher.data_dragon.profile_icons(version)['data']
    summoner_spells = watcher.data_dragon.summoner_spells(version)['data']

    # runes = watcher.data_dragon.runes(version) not working??

    context = {"summonerData": summoner_data, "matches": match_list, "leagues": league_data, 
                "champions": champions, "items": items, "profile_icons": profile_icons, 
                "summoner_spells": summoner_spells, "champion_ids": champion_ids}

    return render(request, 'summoner/home.html', context)

def about(request):
    return render(request, 'summoner/about.html', {"title": "about"}) 