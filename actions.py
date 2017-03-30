from __future__ import print_function
import re
import json
import requests

def sendResponse(event,result=0):
    url = "https://slack.com/api/chat.postMessage"
    if result:
        text = event["amount"] + " " + event["source"] + " is " + str(result) + " " + event["target"]
    else:
        text = event["reply"]
    payload = {"token": event["bot"]["bot_access_token"], "channel": event["event"]["channel"], "text": text}
    response = requests.post(url, data=payload)
    response_json = response.json()
    print(payload)
    event.update(response_json)
    return event
def callFixer(event):
    url = "http://api.fixer.io/latest"
    payload = {"base": event["source"], "symbols": event["target"]}
    response = requests.get(url, params=payload)
    response_json = response.json()
    event.update(response_json)
    result = response_json["rates"][event["target"]] * float(event["amount"])
    print(result)
    sendResponse(event,result)
def doCommand(event):
    command = re.split("> ",event["event"]["text"],maxsplit=1)[1]
    m = re.match("[a-zA-Z\s]*(\d+\.?\d*).*([a-zA-Z]{3}).*([a-zA-Z]{3})",command)
    if bool(m):
        commandParams = {"amount": m.group(1), "source": m.group(2).upper(), "target": m.group(3).upper()}
        print(commandParams)
        event.update(commandParams)
        print(event)
        callFixer(event)
        return event
    reply = "Not my Job Bro! Please enter something like 'Convert 1 AUD to USD'"
    event.update({"reply": reply})
    print(event)
    sendResponse(event)
    return event
def log(event):
    print(json.dumps(event))
def lambda_handler(event,context):
    log(event)
    doCommand(event)
