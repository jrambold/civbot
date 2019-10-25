from django.utils import timezone

def help():
    response = {}
    response["response_type"] = "ephemeral"
    response["text"] = "*Available Commands*"
    response["attachments"] = [
                                {"text":"Under Construction"},
                              ]
    return response
