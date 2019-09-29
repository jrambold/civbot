from civbot.models import Game, Player
from django.utils import timezone
import django_rq
import leaguebot.services.riotapi as rapi

def help():
    response = {}
    response["response_type"] = "ephemeral"
    response["text"] = "Available Commands"
    response["attachments"] = [
                                {"text":"help - How do you think you got here?"},
                                {"text":"add [playername] - add player and game history to bot"},
                              ]
    return response

def add(name):
    response = {}
    try:
        Player.objects.get(name__iexact = name)
        response["text"] = "Player already exists"
        response["response_type"] = "ephemeral"
        return response
    except:
        pass

    player = rapi.addPlayer(name)

    # django_rq.enqueue(rapi.populate_solo, player)
    # django_rq.enqueue(rapi.populate_flex, player)

    if player is None:
        response["text"] = "Invalid Riot Response"
        response["response_type"] = "ephemeral"
    else:
        response["text"] = "Player Added. Populating Games"
        response["response_type"] = "ephemeral"

    return response
