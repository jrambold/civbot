from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
from django.conf import settings
import json
import requests
import friendbets.modulos.notifications as notes
import friendbets.modulos.interactions as interact

def index(request):
    return HttpResponse("Hello World")

#slack slash command url
@csrf_exempt
def command(request):
    try:
        slackCommand = parse_qs(request.body.decode('utf-8', "ignore"))
        text = slackCommand['text'][0].split(' ', 1)
        text[0] = text[0].lower()
    except:
        return HttpResponse('Invalid Request')

    if slackCommand['token'][0] != settings.SLACK_TOKEN_FRIENDBETS:
        return HttpResponse('Invalid Request')

    response = {}

    #all text matches here need to be lowercase for case insensitivity in commands
    if text[0] == 'help':
        response = interact.help()
    else:
        response["response_type"] = "ephemeral"
        response["text"] = "Not a command. User error. Meaning <@" + slackCommand['user_id'][0] + '> fucked up!'

    return JsonResponse(response)
