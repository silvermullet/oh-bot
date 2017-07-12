import logging
import time
import os

import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def build_response(message):
    topics = ""
    for i, j in enumerate(message['Items']):
        topics += "{0}: {1}\n".format(i + 1, j['topic'])

    return {
        "dialogAction":  {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                    "contentType": "PlainText",
                    "content": topics
            }
        }
    }

def lookup_discussion_topics(event, context):
    #debug print for lex event data
    print(event)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_TOPICS'])
    team  = event['currentIntent']['slots']['GetTeam']
    date  = event['currentIntent']['slots']['GetQueryDay']

    filter_expression = Key('date').eq(date) & Key('team').eq(team);
    response = table.scan(
        FilterExpression=filter_expression,
    )

    print("Query succeeded:")

    return build_response(response)
