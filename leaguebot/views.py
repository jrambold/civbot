from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
from django.conf import settings
import json
import leaguebot.modulos.notifications as notes
import leaguebot.modulos.interactions as interact

def index(request):
    return HttpResponse("Hello World")

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
            response["text"] = "Must supply a username"

    elif text[0] == 'stats':
        if len(text) > 1 and len(text[1]) > 0:
            response = interact.stats(text[1])
        else:
            response["response_type"] = "ephemeral"
            response["text"] = "Must supply a username"

    elif text[0] == 'solo':
        response = interact.soloRanks()

    elif text[0] == 'flexLadder':
        response = interact.flexRanks()

    elif text[0] == 'tftLadder':
        response = interact.tftRanks()

    elif text[0] == 'worstSoloChamps':
        response = interact.worstSoloChamps()

    elif text[0] == 'worstFlexChamps':
        response = interact.worstSoloChamps()

    else:
        response["response_type"] = "ephemeral"
        response["text"] = "Not a command. User error. Meaning <@" + slackCommand['user_id'][0] + '> fucked up!'

    return JsonResponse(response)
