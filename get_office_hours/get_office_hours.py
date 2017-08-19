import logging
import json
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
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

def get_office_hours(event, context):
    logger.info('Lex event: {}'.format(event))
    table    = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    team     = event['currentIntent']['slots']['GetTeam']

    try:
        response = table.get_item(
            Key={
                'team': team
            }
        )
    except ClientError as e:
        logger.error("ClientError: {}".format(e.response['Error']['Message']))
    else:
        try:
            item = response['Item']
            logger.info('GetItem succeeded:')
        except KeyError as e:
            logger.error("GetItem item not found: {}".format(e))
            return build_response("Office hours not set for this team presently")
        else:
            return build_response("""{0} is holding office hours on {1} at {2}.
                Office hours starts at {3} and ends at {4}""".format(
                team,
                item['day'],
                item['OfficeHoursLocation'],
                item['SetOfficeHoursStart'],
                item['SetOfficeHoursEnd']))
