from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from civbot.models import Game, Player
from urllib.parse import parse_qs
from django.utils import timezone
from django.conf import settings
import json
import civbot.modulos.notifications as notes
import civbot.modulos.interactions as interact

def root(request):
    return HttpResponse("Hello World")

#webhook url
@csrf_exempt
def index(request):
    try:
        info = json.loads(request.body)
        player = info['value2']
        game = info['value1']
        turn = int(info['value3'])
    except:
        notes.sendSlack('invalid webhook received', '#bot-testing')
        notes.sendSlack(request.body, '#bot-testing')
        return HttpResponse("Invalid Request")

    try:
        game_player = Game.objects.get(name = game, player = player)
        if game_player.turn == turn: #duplicate webhook check
            return JsonResponse(info)
        game_player.turn = turn
        game_player.updated = timezone.now()
    except:
        game_player = Game(name = game, player = player, turn = turn)

    game_player.save()
    game_player.refresh_from_db()

    notes.sendPlayerNotices(game_player)

    return JsonResponse(info)

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
