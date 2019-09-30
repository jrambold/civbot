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

    response["response_type"] = "in_channel"
    response["text"] = player.name + '\'s stats:'
    response["attachments"] = [
                                {"text":
                                    "Solo Queue: " + rank.solo_tier + ' ' + rank.solo_rank + ' ' + str(rank.solo_lp) + 'lp\n'
                                    + '\t' + str(rank.solo_wins) + ' wins ' + str(rank.solo_losses) + ' losses ' + str(round(rank.solo_wins/(rank.solo_wins + rank.solo_losses)*100,1)) + '%'
                                },
                                {"text":
                                    "Flex Queue: " + rank.flex_tier + ' ' + rank.flex_rank + ' ' + str(player.rank.flex_lp) + 'lp\n'
                                    + '\t' + str(rank.flex_wins) + ' wins ' + str(rank.flex_losses) + ' losses ' + str(round(rank.flex_wins/(rank.flex_wins + rank.flex_losses)*100,1)) + '%'
                                },
                                {"text":
                                    "TFT: " + rank.tft_tier + ' ' + rank.tft_rank + ' ' + str(rank.tft_lp) + 'lp\n'
                                    + '\t' + str(rank.tft_wins) + ' wins ' + str(rank.tft_losses) + ' losses ' + str(round(rank.tft_wins/(rank.tft_losses + rank.tft_losses)*100,1)) + '%'
                                },
                              ]
    return response

def soloRanks():
    response = {}
    return response

def flexRanks():
    response = {}
    return response

def tftRanks():
    response = {}
    return response

def worstSoloChamps():
    response = {}
    response["attachments"] = []

    players = Player.objects.all()

    for player in players:
        champs = player.solomatch_set.values_list('champion').distinct()
        champion = 0
        result = 2
        for champ in champs:
            matches = player.solomatch_set.filter(champ[0])
            total = matches.count()
            if total > 5:
                rate = matches.filter(win=True).count()/total
                if rate < result:
                    result = rate
                    champion = champ[0]
        response["attachments"].append({"text": player.name + ': ' + str(champion) + ' winrate: ' + str(round(result*100,1)) + '%'})

    response["response_type"] = "in_channel"
    response["response_type"] = "ephemeral"
    response["text"] = 'Worst Champs (min 5):'

    return response

def worstFlexChamps():
    # response = {}
    # response["attachments"] = []
    #
    # players = Player.objects.all()
    #
    # for player in players:
    #     champs = player.flexmatch_set.values_list('champion').distinct()
    #     champion = 0
    #     result = 2
    #     for champ in champs:
    #         matches = player.flexmatch_set.filter(champ)
    #         total = matches.count()
    #         if total > 5:
    #             rate = matches.filter(win=True).count()/total
    #             if rate < result:
    #                 result = rate
    #                 champion = champ
    #     response["attachments"].append({"text": player.name + ': ' + str(champion) + ' winrate: ' + str(round(result*100,1)) + '%'})

    response["response_type"] = "in_channel"
    response["text"] = 'Worst Champs (min 5):'

    return response
