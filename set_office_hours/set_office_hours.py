import logging
import json
import os
import boto3
from botocore.exceptions import ClientError

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

def set_office_hours(event, context):
    logger.info("build_response to Lex: {}".format(message))

    table    = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    day      = event['currentIntent']['slots']['SetOfficeHoursDays']
    location = event['currentIntent']['slots']['SetOfficeHoursLocation']
    start    = event['currentIntent']['slots']['SetOfficeHoursStart']
    end      = event['currentIntent']['slots']['SetOfficeHoursEnd']
    team     = event['currentIntent']['slots']['SetTeam']

    try:
        response = table.update_item(
            Key={
                'team': team,
                'day': day
            },
            UpdateExpression="set OfficeHoursLocation = :l, SetOfficeHoursStart=:s, SetOfficeHoursEnd=:e, SetOfficeHoursDays=:d",
            ExpressionAttributeValues={
                ':d': day,
                ':l': location,
                ':s': start,
                ':e': end
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        logger.error("ClientError: {}".format(e.response['Error']['Message']))
        response = table.put_item(
            Item={
                'team': team,
                'day': day,
                'OfficeHoursLocation': location,
                'SetOfficeHoursStart': start,
                'SetOfficeHoursEnd': end
                }
            )
        logger.info("new PutItem succeeded:")
    else:
        logger.info("UpdateItem succeeded:")
    return build_response("Office hours set successfully!")
