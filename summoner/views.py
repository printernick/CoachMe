from django.shortcuts import render
import logging
import os

from .scripts.summoner import riotRequestFunctions as riot
from riotwatcher import RiotWatcher, ApiError
posts = [
    {
        'author': 'Oogie Boogie',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'November 20, 2019'
    },
    {
        'author': 'Oogie Troogie',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'November 30, 2019'
    },

]

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

    match_list = watcher.match.matchlist_by_account(region, summoner_data["accountId"])
    league_data = watcher.league.by_summoner(region, summoner_data["id"])

    #Static content
    version = watcher.data_dragon.versions_for_region(region)['v']
    champions = watcher.data_dragon.champions(version)
    items = watcher.data_dragon.items(version)
    profile_icons = watcher.data_dragon.profile_icons(version)
    summoner_spells = watcher.data_dragon.summoner_spells(version)

    # runes = watcher.data_dragon.runes(version) not working??

    context = {"summonerData": summoner_data, "matches": match_list['matches'], "leagues": league_data, 
                "champions": champions, "items": items, "profile_icons": profile_icons, 
                "summoner_spells": summoner_spells}

    return render(request, 'summoner/home.html', context)

def about(request):
    return render(request, 'summoner/about.html', {"title": "about"}) 