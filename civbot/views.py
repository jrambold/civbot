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
    response = {}
    slackCommand = parse_qs(request.body.decode('utf-8', "ignore"))

    text = slackCommand['text'][0].split(' ', 1)

    if text[0] == 'help':
        response["response_type"] = "ephemeral"
        response["text"] = "Available Commands"
        response["attachments"] = [
                                    {"text":"help - How do you think you got here?"},
                                    {"text":"game [gamename] - Tells you info about the game"}
                                  ]
    elif text[0] == 'game':
        game_query = Game.objects.filter(name__iexact = text[1]).order_by('updated')
        if game_query.count() > 0:
            response["text"] = "Turn: " + str(game_query.last().turn)
            response["attachments"] = []
            for game in game_query:
                response["attachments"].append({"text": game.player})
            response["attachments"][-1]['text'] =  'Current Turn: ' + response["attachments"][-1]['text']
        else:
            response["text"] = "Game not found"
        response["response_type"] = "in_channel"
    elif text[0] == 'gamelist':
        game_query = Game.objects.all().order_by('updated').distinct('name')
        game_list = "Current Games:\n"
        # for game in game_query:
        #     game_list = game_list + game.name + ' Turn: ' + str(game.turn) + ' Last Played on: ' + game.updated + '\n'
        response["text"] = gamelist
        # response["response_type"] = "in_channel"
    else:
        response["response_type"] = "ephemeral"
        response["text"] = "Not a command. User error. User meaning you <@" + slackCommand['user_id'][0] + '>!'

    return JsonResponse(response)
