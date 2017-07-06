import logging
import json
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

def set_office_hours(event, context):
    #debug print for lex event data
    print(event)

    table    = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    date     = event['currentIntent']['slots']['SetOfficeHoursDay']
    location = event['currentIntent']['slots']['SetOfficeHoursLocation']
    start    = event['currentIntent']['slots']['SetOfficeHoursStart']
    end      = event['currentIntent']['slots']['SetOfficeHoursEnd']
    team     = event['currentIntent']['slots']['SetTeam']

    response = table.put_item(
        Item={
            'id': team + date,
            'team': team,
            'date': date,
            'OfficeHoursLocation': location,
            'SetOfficeHoursStart': start,
            'SetOfficeHoursEnd': end
        }
    )

    print("PutItem succeeded:")

    return build_response("Office hours set successfully!")
