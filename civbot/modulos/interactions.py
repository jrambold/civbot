from civbot.models import Game, Player

def help():
    response = {}
    response["response_type"] = "ephemeral"
    response["text"] = "Available Commands"
    response["attachments"] = [
                                {"text":"help - How do you think you got here?"},
                                {"text":"gamelist - Lists the current games tracked"},
                                {"text":"game [gamename] - Tells you info about the game"},
                              ]
    return response

def game(name):
    response = {}
    game_query = Game.objects.filter(name__iexact = name).order_by('updated')
    if game_query.count() > 0:
        response["text"] = "Last Turn Taken: " + game_query.last().updated.strftime("%m/%d/%Y, %I:%M%p") + "\nTurn: " + str(game_query.last().turn)  + "\nPlayers:\n"
        response["attachments"] = []
        player_list = ""
        for game in game_query:
            player_list = player_list + "\n" + game.player + " Started Turn: " + game.updated.strftime("%m/%d/%Y, %I:%M%p")
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
        game_list = game_list + game.name + ' - Turn: ' + str(game.turn) + ' - Last Turn: ' + game.updated.strftime("%m/%d/%Y, %I:%M%p") + '\n'
    response["text"] = str(game_list)
    response["response_type"] = "in_channel"
    return response
