from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from civbot.models import Game, Player
import os
import slack
import json
import civbot.notifications as notes

def root(request):
    return HttpResponse("Hello World")

def index(request):
    info = json.loads(request.body)

    try:
        player = info['value2']
        game = info['value1']
        turn = int(info['value3'])
    except:
        note.sendSlack(info)
        return JsonResponse(info)

    try:
        game_player = Game.objects.get(name = game, player = player)
        if game_player.turn == turn:
            return JsonResponse(info)
        game_player.turn = turn
    except:
        game_player = Game(name = game, player = player, turn = turn)

    game_player.save()
    game_player.refresh_from_db()

    notes.sendAll(game)

    return JsonResponse(info)
