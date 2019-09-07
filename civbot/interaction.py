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
    game_query = Game.objects.filter(name__iexact = name).order_by('updated')
    if game_query.count() > 0:
        response["text"] = "Last Turn Taken: " + game_query.last().updated.strftime("%m/%d/%Y, %H:%M") + "\nTurn: " + str(game_query.last().turn)
        response["attachments"] = []
        for game in game_query:
            response["attachments"].append({"text": game.player})
        response["attachments"][-1]['text'] =  'Current Turn: ' + response["attachments"][-1]['text']
        response["response_type"] = "in_channel"
    else:
        response["text"] = "Game not found"
        response["response_type"] = "ephemeral"

    return response

def gamelist():
    game_list = "Current Games: \n"
    game_query = Game.objects.order_by('name', '-updated').distinct('name')
    for game in game_query:
        game_list = game_list + game.name + ' - Turn: ' + str(game.turn) + ' - Last Turn: ' + game.updated.strftime("%m/%d/%Y, %H:%M") + '\n'
    response["text"] = str(game_list)
    response["response_type"] = "in_channel"
    return response
