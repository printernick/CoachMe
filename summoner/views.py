from django.shortcuts import render
import logging
import os

from .scripts.summoner import riotRequestFunctions as riot
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
    # if request.method == 'POST':
    #     logging.debug("I am a post request")
    # else:
    #     print("goodbye")
    # context = {
    #     'posts': posts
    # }
    summoner_name = request.GET.get('summoner_name')
    region = request.GET.get("region")

    cur_path = os.getcwd()
    file = open(os.path.join(cur_path, '_info', 'api.txt'), "r")
    APIKey = file.read()

    summoner_data = riot.requestSummonerData(region, summoner_name, APIKey)

    # if summoner not found
    if "status" in summoner_data:
        return render(request, "summoner/error.html", {"summonerData": {"name": summoner_name}})

    match_list = riot.requestMatchlist(region, summoner_data["accountId"], APIKey)

    context = {"summonerData": summoner_data, "matches": match_list}

    return render(request, 'summoner/home.html', context)

def about(request):
    return render(request, 'summoner/about.html', {"title": "about"}) 