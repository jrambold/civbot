from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from civbot.models import Game, Player
import json
import civbot.notifications as notes
from urllib.parse import parse_qs

def root(request):
    return HttpResponse("Hello World")

@csrf_exempt
def index(request):
    info = json.loads(request.body)

    try:
        player = info['value2']
        game = info['value1']
        turn = int(info['value3'])
    except:
        notes.sendSlack(info)
        return JsonResponse(info)

    try:
        game_player = Game.objects.get(name = game, player = player)
        if game_player.turn == turn: #duplicate webhook check
            return JsonResponse(info)
        game_player.turn = turn
    except:
        game_player = Game(name = game, player = player, turn = turn)

    game_player.save()
    game_player.refresh_from_db()

    notes.sendAll(game_player)

    return JsonResponse(info)

@csrf_exempt
def command(request):
    things = parse_qs(request.body)
    notes.sendSlackTest(str(things))
    return JsonResponse(things, safe=False)
