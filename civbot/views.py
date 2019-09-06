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
    slackCommand = parse_qs(request.body.decode('utf-8', "ignore"))

    response = {}
    response["response_type"] = "ephemeral"
    response["text"] = "Not a command. User error. User meaning you <@"

    # text = slackCommand['text'].split(' ')
    #
    # response = {}
    #
    # if text[0] == 'help':
    #     response["response_type"] = "ephemeral"
    #     response["text"] = "I'm still building it asshole. Hold your horses"
    #     response["attachments"] = [
    #                                 {"text":"help - How do you think you got here?"},
    #                                 {"text":"game [gamename] - Tells you info about the game"}
    #                               ]
    # elif text[0] == 'game':
    #     response["response_type"] = "in_channel"
    #     response["text"] = "I'm still building it asshole. Hold your horses"
    # else:
    #     response["response_type"] = "ephemeral"
    #     response["text"] = "Not a command. User error. User meaning you <@" + slackCommand['user_id'] + '>!'

    return JsonResponse(response)
