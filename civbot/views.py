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
    info = json.dumps(request.POST)
    client = slack.WebClient(token=settings.SLACK_CIVBOT)
    starterbot_id = None
    response = client.chat_postMessage(
        channel='#bot-testing',
        text=info)
    assert response["ok"]
    assert response["message"]["text"] == info
    return JsonResponse(json.loads(info))
