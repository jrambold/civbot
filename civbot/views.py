from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from civbot.models import Game, Player
import os
import slack
import json
from .notifications import getSlackId

def root(request):
    return HttpResponse("Hello World")

@csrf_exempt
def index(request):
    info = json.loads(request.body)

    try:
        player = info['value2']
        game = info['value1']
        turn = info['value3']
    except:
        message = info
        client = slack.WebClient(token=settings.SLACK_CIVBOT)
        response = client.chat_postMessage(
            channel='#civilization',
            text=message)
        return JsonResponse(info)

    game_player = Game.objects.filter(name = game, player = player)
    name = models.CharField(max_length=200)
    player = models.CharField(max_length=200)
    player = getSlackId(player)
    message = "Hey " + player + " it's your turn in " + game + ".\nTurn: " + turn





    except:
        message = info

    client = slack.WebClient(token=settings.SLACK_CIVBOT)
    response = client.chat_postMessage(
        channel='#civilization',
        text=message)
    # assert response["ok"]
    return JsonResponse(info)
