import logging
import json
import os
import uuid
import boto3
from botocore.exceptions import ClientError

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
    #debug print for lex event data
    print(event)

    table    = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    day      = event['currentIntent']['slots']['SetOfficeHoursDay']
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
            UpdateExpression="set OfficeHoursLocation = :l, SetOfficeHoursStart=:s, SetOfficeHoursEnd=:e, SetDays=:d",
            ExpressionAttributeValues={
                ':d': day,
                ':l': location,
                ':s': start,
                ':e': end
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        response = table.put_item(
            Item={
                'team': team,
                'day': day,
                'OfficeHoursLocation': location,
                'SetOfficeHoursStart': start,
                'SetOfficeHoursEnd': end
                }
            )
        print("new PutItem succeeded:")
    else:
        print("UpdateItem succeeded:")
    return build_response("Office hours set successfully!")
