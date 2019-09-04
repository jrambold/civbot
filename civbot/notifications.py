from civbot.models import Game, Player
def sendAll(game):
    usercomp = {
        'wraithcube': '<@U33KZ0E95>',
        'cowtastic': '<@U32S2CLTU>',
        'dejavood0o': '<@U32UN4LGM>',
        'pouchnort': '<@U33Q58S3E>',
        'mr goopy daddy': '<@U33HC4X0E>',
        'spadefish': '<@U35MSNBUM>',
        'kalamari tank': '<@U32U6FD50>',
        'davis': '<@U32UUHARF>',
        'hack': '<@UMPH45VPT>',
    }
    name = game.player.lower()
    if name in usercomp:
        name = usercomp[name]

    message = "Hey " + name + " it's your turn in " + game.game + ".\nTurn: " + str(game.turn)
    sendSlack(message)
    return message

def sendSlack(message):
    client = slack.WebClient(token=settings.SLACK_CIVBOT)
    response = client.chat_postMessage(
        channel='#civilization',
        text=message)
    return message
