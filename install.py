from __future__ import print_function
import json
import os
import requests
import boto3

def saveResponse(token_json):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TEAMS_TABLE"])
    table.put_item(Item = token_json)
def requestToken(code):
    print("Requesting token for " + code)
    if not code:
        return None
    post_data = {
    "client_id": os.environ['CLIENT_ID'],
    "client_secret": os.environ['CLIENT_SECRET'],
    "grant_type": "authorization_code",
    'code': code
    }
    url = 'https://slack.com/api/oauth.access'
    response = requests.post(url, data=post_data)
    token_json = response.json()
    return token_json
def lambda_handler(event, context):
    code = event['code']
    res = requestToken(code)
    saveResponse(res)
    return res
