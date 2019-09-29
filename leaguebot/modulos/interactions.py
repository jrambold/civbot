from leaguebot.models import Player, Rank, SoloMatch, FlexMatch
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
                                {"text":"refresh [playername] - update players stats and games"},
                                {"text":"stats [playername] - show players rankings"},
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
    player = rapi.getRanks(player)

    django_rq.enqueue(rapi.populate_solo, player)
    django_rq.enqueue(rapi.populate_flex, player)

    if player is None:
        response["text"] = "Invalid Riot Response"
        response["response_type"] = "ephemeral"
    else:
        response["text"] = "Player Added. Populating Games"
        response["response_type"] = "ephemeral"

    return response

def refresh(name):
    response = {}
    try:
        player = Player.objects.get(name__iexact = name)
    except:
        response["text"] = "Player Not Found. Try add"
        response["response_type"] = "ephemeral"
        return response

    player = rapi.getRanks(player)

    django_rq.enqueue(rapi.populate_solo, player)
    django_rq.enqueue(rapi.populate_flex, player)

    response["text"] = "Player Refreshed. Adding Games"
    response["response_type"] = "ephemeral"

    return response

def stats(name):
    response = {}

    try:
        player = Player.objects.get(name__iexact = name)
    except:
        response["text"] = "Player Not Found. Try add"
        response["response_type"] = "ephemeral"
        return response

    rank = player.rank

    response["response_type"] = "ephemeral"
    # response["response_type"] = "in_channel"
    response["text"] = player.name + '\'s stats:'
    response["attachments"] = [
                                {"text":
                                    "Solo Queue: " + rank.solo_tier + ' ' + rank.solo_rank + ' ' + str(rank.solo_lp) + 'lp\n'
                                    # + '\t' + rank.solo_wins + ' wins ' + rank.solo_losses + ' losses ' + round(rank.solo_wins/rank.solo_losses,1) + '%'
                                },
    #                             {"text":
    #                                 "Flex Queue: " + rank.flex_tier + ' ' + rank.flex_rank + ' ' + player.rank.flex_lp + 'lp\n'
    #                                 + '\t' + rank.flex_wins + ' wins ' + rank.flex_losses + ' losses ' + round(rank.flex_wins/rank.flex_losses,1) + '%'
    #                             },
    #                             {"text":
    #                                 "TFT: " + rank.tft_tier + ' ' + rank.tft_rank + ' ' + rank.tft_lp + 'lp\n'
    #                                 + '\t' + rank.tft_wins + ' wins ' + rank.tft_losses + ' losses ' + round(rank.tft_wins/rank.tft_losses,1) + '%'
    #                             },
                              ]
    return response
