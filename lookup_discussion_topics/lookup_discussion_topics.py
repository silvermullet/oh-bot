import logging
import time
import os

import boto3
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')

def build_response(message):
    logger.info("build_response to Lex: {}".format(message))
    topics = ""
    for i, j in enumerate(message['Items']):
        topics += "{0}: {1} - submitted by {2}\n".format(
            i + 1,
            j['topic'],
            j['user'])

    if not topics:
        topics = "No topics for this date have been set"

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
    logger.info("Lex event: {}".format(event))

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_TOPICS'])
    team  = event['currentIntent']['slots']['GetTeam']
    date  = event['currentIntent']['slots']['GetQueryDay']

    filter_expression = Key('date').eq(date) & Key('team').eq(team);
    response = table.scan(
        FilterExpression=filter_expression,
    )

    logger.info("Query succeded:")

    return build_response(response)
