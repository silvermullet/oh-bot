import logging
import time
import decimal

from todos import decimalencoder
import boto3

dynamodb = boto3.client('dynamodb')

def set_office_hours(event, context):
    #debug print for lex event data
    print(event)

    data = json.loads(event['body'])

    if 'office_hours_location' not in data:
        logging.error("Validation Failed")
        raise Exception("Could not set office hours")
        return

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    today = time.strftime("%d/%m/%Y")

    response = table.put_item(
        Item={
            'date': today,
            'slack_team': data['slack_team'],
            'slack_channel': data['slack_channel'],
            'office_hours_location': data['office-hours-location'],
        }
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))

    return response
