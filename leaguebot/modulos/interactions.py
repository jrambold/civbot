from civbot.models import Game, Player
from django.utils import timezone

def help():
    response = {}
    response["response_type"] = "ephemeral"
    response["text"] = "Available Commands"
    response["attachments"] = [
                                {"text":"help - How do you think you got here?"},
                                {"text":"gamelist - Lists the current games tracked"},
                                {"text":"game [gamename] - Tells you info about the game"},
                                {"text":"yell [gamename] - Yells at whoever's turn it is in the game"},
                              ]
    return response

def add(name):
    response = {}
    game_query = Game.objects.filter(name__iexact = name).order_by('updated')
    if game_query.count() > 0:
        response["text"] = "Last Turn Taken: " + timezone.localtime(game_query.last().updated).strftime("%m/%d/%Y, %I:%M%p") + "\nTurn: " + str(game_query.last().turn)  + "\nPlayers:\n"
        response["attachments"] = []
        player_list = ""
        for game in game_query:
            player_list = player_list + "\n" + game.player + " Started Turn: " + timezone.localtime(game.updated).strftime("%m/%d/%Y, %I:%M%p")
        player_list = player_list + " - Current Turn"
        response["attachments"] = [{"text": player_list}]
        response["response_type"] = "in_channel"
    else:
        response["text"] = "Game not found"
        response["response_type"] = "ephemeral"

    return response

def gamelist():
    response = {}
    game_list = "Current Games: \n"
    game_query = Game.objects.order_by('name', '-updated').distinct('name')
    for game in game_query:
        game_list = game_list + game.name + ' - Turn: ' + str(game.turn) + ' - Last Turn: ' + timezone.localtime(game.updated).strftime("%m/%d/%Y, %I:%M%p") + '\n'
    response["text"] = str(game_list)
    response["response_type"] = "in_channel"
    return response

def yell(name):
    response = {}
    game = Game.objects.filter(name__iexact = name).order_by('-updated').first()
    if game is not None:
        try:
            player = Player.objects.get(steamName__iexact=game.player)
        except:
            response["text"] = "No slack info for " + game.player + " found"
            response["response_type"] = "ephemeral"
            return response

        if player.slackId is None:
            name = player.steamName
        else:
            name = '<@' + player.slackId + '>'

        response["text"] = "Hey " + name + " hurry up and go in " + game.name

        diff = timezone.now() - game.updated
        hours = diff.days * 24 + diff.seconds // 3600

        text = "\nIt's been your turn since " + timezone.localtime(game.updated).strftime("%m/%d/%Y, %I:%M%p")
        text = text + "\nThat was " + str(hours) + " hours ago!"
        response["attachments"] = [{'text': text}]
        response["response_type"] = "in_channel"
    else:
        response["text"] = "Game not found"
        response["response_type"] = "ephemeral"
    return response
