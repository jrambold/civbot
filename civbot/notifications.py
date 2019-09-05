from civbot.models import Game, Player
def sendAll(game):
    try:
        user = player.objects.get(steamName=game.player)
    except:
        message = "It's " + game.player + "'s your turn in' " + game.game + ".\nTurn: " + str(game.turn) + "\nPlayer unknown to CivBot"
        sendSlack(message)

    if user.slackNotification:
        name = '<@' + user.slackId + '>'
        message = "Hey " + name + " it's your turn in " + game.game + ".\nTurn: " + str(game.turn)
        sendSlack(message)

    if user.emailNotification:
        pass

    if user.discordNotification:
        pass

    return message

def sendSlack(message):
    client = slack.WebClient(token=settings.SLACK_CIVBOT)
    response = client.chat_postMessage(
        channel='#civilization',
        text=message)
    return message
