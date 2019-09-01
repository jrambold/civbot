import os
import slack

client = slack.WebClient(token='xoxb-104210651201-746975311638-8giFxUsPeEtgyEMzQ6SJv8fV')

starterbot_id = None

response = client.chat_postMessage(
    channel='#bot-testing',
    text="Hello world!")
assert response["ok"]
assert response["message"]["text"] == "Hello world!"
