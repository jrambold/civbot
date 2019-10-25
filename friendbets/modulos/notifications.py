from django.conf import settings
import slack

def sendSlack(message, channel):
    client = slack.WebClient(token=settings.SLACK_FRIENDBETS)
    response = client.chat_postMessage(
        channel=channel,
        text=message)
    return message
