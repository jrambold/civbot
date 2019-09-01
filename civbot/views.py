from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import slack
import json
from .userlist import getSlackId

def root(request):
    return HttpResponse("Hello World")

@csrf_exempt
def index(request):
    info = json.loads(request.body)

    try:
        name = info['value2']
        game = info['value1']
        turn = info['value3']

        name = getSlackId(name)

        message = "Hey " + name + " it's your turn in " + game + ".\nTurn: " + turn
    except:
        message = info

    client = slack.WebClient(token=settings.SLACK_CIVBOT)
    starterbot_id = None
    response = client.chat_postMessage(
        channel='#civilization',
        text=message)
    # assert response["ok"]
    return JsonResponse(info)
