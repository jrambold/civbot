from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import slack
import json

def root(request):
    return HttpResponse("Hello World")

@csrf_exempt
def index(request):
    info = json.loads(request.body)

    try:
        message = "Hey @" + info['value2'] + " it's your turn in " + info['value1'] + ". Turn:" + info['value3']
    except:
        message = "Cibot Error"

    client = slack.WebClient(token=settings.SLACK_CIVBOT)
    starterbot_id = None
    response = client.chat_postMessage(
        channel='#civilization',
        text=message)
    # assert response["ok"]
    # assert response["message"]["text"] == info
    return JsonResponse(info)
