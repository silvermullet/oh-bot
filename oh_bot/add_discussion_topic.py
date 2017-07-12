import logging
import time
import os
import uuid

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

def add_discussion_topic(event, context):
    #debug print for lex event data
    print(event)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_TOPICS'])
    team  = event['currentIntent']['slots']['GetTeam']
    date  = event['currentIntent']['slots']['GetDay']
    topic = event['currentIntent']['slots']['GetTheTopic']

    response = table.put_item(
        Item={
            'id': str(uuid.uuid1()),
            'team': team,
            'date': date,
            'topic': topic
        }
    )

    print("PutItem succeeded:")

    return build_response("topic added!")
