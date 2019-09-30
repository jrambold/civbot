from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
from django.conf import settings
import json
import requests
import leaguebot.modulos.notifications as notes
import leaguebot.modulos.interactions as interact
from leaguebot.models import Champion

def index(request):
    return HttpResponse("Hello World")

def updateChamps(request):
    r = requests.get(f"http://ddragon.leagueoflegends.com/cdn/9.19.1/data/en_US/champion.json").json()
    for key in r['data'].keys():
        champion = r['data'][key]
        tag1 = champion['tags'][0]
        if len(champion['tags']) > 1:
            tag2 = champion['tags'][1]
        else:
            tag2 = None
        stats = champion['stats']
        champ = Champion(
                        id = champion['key'],
                    	name = champion['name'],
                    	version = champion['version'],
                    	title = champion['title'],
                    	blurb =  champion['blurb'],
                    	tag1 = tag1,
                    	tag2 = tag2,
                    	partype = champion['partype'],
                    	hp = stats['hp'],
                    	hpperlevel = stats['hpperlevel'],
                    	mp = stats['mp'],
                    	mpperlevel = stats['mpperlevel'],
                    	movespeed = stats['movespeed'],
                    	armor = stats['armor'],
                    	armorperlevel = stats['armorperlevel'],
                    	spellblock = stats['spellblock'],
                    	spellblockperlevel = stats['spellblockperlevel'],
                    	attackrange = stats['attackrange'],
                    	hpregen = stats['hpregen'],
                    	hpregenperlevel = stats['hpregenperlevel'],
                    	mpregen = stats['mpregen'],
                    	mpregenperlevel = stats['mpregenperlevel'],
                    	crit = stats['crit'],
                    	critperlevel = stats['critperlevel'],
                    	attackdamage = stats['attackdamage'],
                    	attackdamageperlevel = stats['attackdamageperlevel'],
                    	attackspeed = stats['attackspeed'],
                    	attackspeedperlevel = stats['attackspeedperlevel'],
                        )
        champ.save()
    return JsonResponse(r, safe=False)

#slack slash command url
@csrf_exempt
def command(request):
    try:
        slackCommand = parse_qs(request.body.decode('utf-8', "ignore"))
        text = slackCommand['text'][0].split(' ', 1)
        text[0] = text[0].lower()
    except:
        return HttpResponse('Invalid Request')

    if slackCommand['token'][0] != settings.SLACK_TOKEN_LEAGUE:
        return HttpResponse('Invalid Request')

    response = {}

    #all text matches here need to be lowercase for case insensitivity in commands
    if text[0] == 'help':
        response = interact.help()

    elif text[0] == 'add':
        if len(text) > 1 and len(text[1]) > 0:
            response = interact.add(text[1])
        else:
            response["response_type"] = "ephemeral"
            response["text"] = "Must supply a username"

    elif text[0] == 'refresh':
        if len(text) > 1 and len(text[1]) > 0:
            response = interact.refresh(text[1])
        else:
            response["response_type"] = "ephemeral"
            response["text"] = "Must supply a username or refreshAll for everyone"

    elif text[0] == 'refreshall':
        response = interact.refreshAll()

    elif text[0] == 'stats':
        if len(text) > 1 and len(text[1]) > 0:
            response = interact.stats(text[1])
        else:
            response["response_type"] = "ephemeral"
            response["text"] = "Must supply a username"

    elif text[0] == 'leaderboard':
        response = interact.leaderboard()

    elif text[0] == 'solo':
        response = interact.soloRanks()

    elif text[0] == 'flexladder':
        response = interact.flexRanks()

    elif text[0] == 'tftLadder':
        response = interact.tftRanks()

    elif text[0] == 'worstsolochamps':
        response = interact.worstSoloChamps()

    elif text[0] == 'worstflexchamps':
        response = interact.worstFlexChamps()

    else:
        response["response_type"] = "ephemeral"
        response["text"] = "Not a command. User error. Meaning <@" + slackCommand['user_id'][0] + '> fucked up!'

    return JsonResponse(response)
