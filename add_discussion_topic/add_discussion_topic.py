import logging
import time
import os
import uuid
from slackclient import SlackClient

import boto3

dynamodb = boto3.resource('dynamodb')
slack_token = os.environ["CLIENT_SECRET"]
sc = SlackClient(slack_token)

def build_response(message):
    return {
        "dialogAction":  {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                    "contentType": "PlainText",
                    "content": message
            }
        }
    }

def trim_userid(userId):
    userids = userId.split(":")
    slack_userId = userids[2]
    return slack_userId

def get_slack_user_id(slack_userId):
    user_info = sc.api_call(
        "users.info",
        user=slack_userId,
    )
    return user_info['user']['real_name']

def add_discussion_topic(event, context):
    #debug print for lex event data
    print(event)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_TOPICS'])
    team  = event['currentIntent']['slots']['GetTeam']
    date  = event['currentIntent']['slots']['GetDay']
    topic = event['currentIntent']['slots']['GetTheTopic']
    user  = get_slack_user_id(trim_userid(event['userId']))

    response = table.put_item(
        Item={
            'id': str(uuid.uuid1()),
            'team': team,
            'date': date,
            'user': user,
            'topic': topic
        }
    )

    print("PutItem succeeded:")

    return build_response("topic added!")
