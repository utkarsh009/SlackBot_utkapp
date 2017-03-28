from __future__ import print_function
import os
import boto3
import re
import json

class TokenException(Exception):
    pass
def invokeAction(params):
    actionFunctionName = os.environ["NAMESPACE"] + "-actions"
    print("Invoking " + actionFunctionName + " with event")
    client = boto3.client('lambda')
    client.invoke(FunctionName=actionFunctionName, InvocationType='Event',LogType='None', Payload=json.dumps(params))
def checkForMention(params):
    pattern = re.compile("<@" + params["bot"]["bot_user_id"] + ">.*$")
    isPresent = bool(pattern.match(params["event"]["text"]))
    if isPresent:
        print("Bot " + params["bot"]["bot_user_id"] + " is mentioned in " + params["event"]["text"])
        invokeAction(params)
def getTeam(params):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TEAMS_TABLE"])
    response = table.get_item(Key={"team_id": params["team_id"]})
    params.update(response['Item'])
def lambda_handler(event,context):
    response = {}
    params = event["postBody"]
    if params["type"] == "url_verification":
        response.update({"challenge": params["challenge"]})
        return response
    if params["token"] != os.environ["VERIFICATION_TOKEN"]:
        raise TokenException("Invalid Token!")
    getTeam(params)
    checkForMention(params)
