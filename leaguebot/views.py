from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from leaguebot.models import Player, FlexMatch, SoloMatch
from urllib.parse import parse_qs
from django.utils import timezone
from django.conf import settings
import requests
import json
import django_rq
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

    if slackCommand['token'][0] != settings.SLACK_TOKEN:
        return HttpResponse('Invalid Request')

    response = {}

    if text[0] == 'help':
        response = interact.help()

    elif text[0] == 'game':
        if len(text) > 1 and len(text[1]) > 0:
            response = interact.game(text[1])
        else:
            response["response_type"] = "ephemeral"
            response["text"] = "Must supply a game name"

    elif text[0] == 'gamelist':
        response = interact.gamelist()

    elif text[0] == 'yell':
        if len(text) > 1 and len(text[1]) > 0:
            response = interact.yell(text[1])
        else:
            response["response_type"] = "ephemeral"
            response["text"] = "Must supply a game name"

    else:
        response["response_type"] = "ephemeral"
        response["text"] = "Not a command. User error. Meaning <@" + slackCommand['user_id'][0] + '> fucked up!'

    return JsonResponse(response)
