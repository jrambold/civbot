from leaguebot.models import Player, Rank, SoloMatch, FlexMatch, Champion
from django.utils import timezone
import django_rq
import leaguebot.services.riotapi as rapi
from django.db.models import F, ExpressionWrapper, FloatField

def help():
    response = {}
    response["response_type"] = "ephemeral"
    response["text"] = "*Available Commands*"
    logistics = ("Adding and Updating Info" +
                    "\n• help - How do you think you got here?"+
                    "\n• add [playername] - add player and game history to bot"+
                    "\n• refreshAll - updates all player ranks and games"+
                    "\n• refresh [playername] - update players ranks and games")
    group = ("Group Stats"+
                    "\n• leaderboard - everyone ranked by win rate"+
                    "\n• worstSoloChamps - everyone's lowest winrate soloqueue champs"+
                    "\n• worstFlexChamps - everyone's lowest winrate flexqueue champs")
    individual = ("Individual Stats"+
                    "\n• stats [playername] - show players rankings")
    response["attachments"] = [
                                {"text":logistics},
                                {"text":group},
                                {"text":individual},
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

def refreshAll():
    response = {}
    django_rq.enqueue(rapi.updateAll)

    response["text"] = "Refreshing Ranks. Loading Games"
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

def leaderboard():
    response = {}
    response["response_type"] = "in_channel"
    response["text"] = 'Leaderboard'
    response["attachments"] = []

    players = Rank.objects.annotate(percent= ExpressionWrapper(100.0 * F('solo_wins') / (F('solo_wins') + F('solo_losses')), output_field=FloatField()) ).order_by('-percent')
    solo = '*Solo Queue Heroes*'
    for rank in players:
        solo = solo + '\n\t' + rank.player.name + ' ' +  str(round(rank.percent,1)) + '% ' + str(rank.solo_wins) + ' wins ' + str(rank.solo_losses) + ' losses (' + rank.solo_tier + ' ' + rank.solo_rank + ')'

    players = Rank.objects.annotate(percent= ExpressionWrapper(100.0 * F('flex_wins') / (F('flex_wins') + F('flex_losses')), output_field=FloatField()) ).order_by('-percent')
    flex = '*Flex Teammates*'
    for rank in players:
        flex = flex + '\n\t' + rank.player.name + ' ' + str(round(rank.percent,1)) + '% ' + str(rank.flex_wins) + ' wins ' + str(rank.flex_losses) + ' losses (' + rank.flex_tier + ' ' + rank.flex_rank + ')'

    players = Rank.objects.annotate(percent= ExpressionWrapper(100.0 * F('tft_wins') / (F('tft_wins') + F('tft_losses')), output_field=FloatField()) ).order_by('-percent')
    tft = '*TFT Strategists*'
    for rank in players:
        tft = tft + '\n\t' + rank.player.name + ' ' +  str(round(rank.percent,1)) + '% '+ str(rank.tft_wins) + ' wins ' + str(rank.tft_losses) + ' losses (' + rank.tft_tier + ' ' + rank.tft_rank + ')'

    response["attachments"].append({"text": solo})
    response["attachments"].append({"text": flex})
    response["attachments"].append({"text": tft})

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
        games = 0
        for champ in champs:
            matches = player.solomatch_set.filter(champion=champ[0])
            total = matches.count()
            if total >= 5:
                rate = (matches.filter(win=True).count())/total
                if rate < result:
                    result = rate
                    champion = champ[0]
                    games = total
        if champion == 0:
            response["attachments"].append({"text": player.name + ': No champion played 5 times'})
        else:
            champ_details = Champion.objects.get(id=champion)
            title = champ_details.title
            if title.startswith('the '):
                title = title.split('the ',1)[1]
            response["attachments"].append({"text": player.name + ': ' + champ_details.name + ' played ' + str(games) + ' times winrate: ' + str(round(result*100,1)) + '%\nA True ' + title})

    response["response_type"] = "in_channel"
    response["text"] = 'Worst Champs (min 5):'

    return response

def worstFlexChamps():
    response = {}
    response["attachments"] = []

    players = Player.objects.all()

    for player in players:
        champs = player.flexmatch_set.values_list('champion').distinct()
        champion = 0
        result = 2
        games = 0
        for champ in champs:
            matches = player.flexmatch_set.filter(champion=champ[0])
            total = matches.count()
            if total >= 5:
                rate = (matches.filter(win=True).count())/total
                if rate < result:
                    result = rate
                    champion = champ[0]
                    games = total
        if champion == 0:
            response["attachments"].append({"text": player.name + ': No champion played 5 times'})
        else:
            champ_details = Champion.objects.get(id=champion)
            title = champ_details.title
            if title.startswith('the '):
                title = title.split('the ',1)[1]
            response["attachments"].append({"text": player.name + ': ' + champ_details.name + ' played ' + str(games) + ' times winrate: ' + str(round(result*100,1)) + '%\nA True ' + title})

    response["response_type"] = "in_channel"
    response["text"] = 'Worst Champs (min 5):'

    return response
