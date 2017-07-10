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

def get_office_hours(event, context):
    #debug print for lex event data
    print(event)
    table    = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    team     = event['currentIntent']['slots']['GetTeam']

    try:
        response = table.get_item(
            Key={
                'team': team
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
        return build_response("""{0} is holding office hours on {1} at {2}.
            Office hours starts at {3} and ends at {4}""".format(
                team, item['day'],
                item['OfficeHoursLocation'], item['SetOfficeHoursStart'],
                item['SetOfficeHoursEnd']))
