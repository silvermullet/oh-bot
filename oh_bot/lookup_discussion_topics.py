import logging
import time
import os

import boto3

dynamodb = boto3.resource('dynamodb')

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

def lookup_discussion_topics(event, context):
    #debug print for lex event data
    print(event)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_TOPICS'])
    team  = event['currentIntent']['slots']['GetTeam']
    date  = event['currentIntent']['slots']['GetQueryDay']

    response = table.query(
        KeyConditionExpression=Key('date').eq(date) & Key('team').eq(team)
    )

    print("Query succeeded:")

    return build_response("topics for discussion: {0}".format(response))
