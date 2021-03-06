from django.conf import settings
from civbot.models import Game, Player
import slack

def sendPlayerNotices(game):
    try:
        user = Player.objects.get(steamName__iexact=game.player)
    except: #User not in database - probably rando or someone needing ot be added
        message = "It's " + game.player + "'s your turn in' " + game.name + ".\nTurn: " + str(game.turn) + "\nPlayer unknown to CivBot"
        sendSlack(message, '#civilization')

    if user.slackNotification:
        if user.slackId is None:
            name = user.steamName
        else:
            name = '<@' + user.slackId + '>'
        message = "Hey " + name + " it's your turn in " + game.name + ".\nTurn: " + str(game.turn)
        sendSlack(message, '#civilization')

    if user.emailNotification:
        pass

    if user.discordNotification:
        pass

    return message

def sendSlack(message, channel):
    client = slack.WebClient(token=settings.SLACK_CIVBOT)
    response = client.chat_postMessage(
        channel=channel,
        text=message)
    return message
