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

    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Could not set office hours")
        return

    table = dynamodb.Table('OfficeHoursBot')
    today = time.strftime("%d/%m/%Y")
    response = table.put_item(
        Item={
            'date': today,
            'location': "pull from lex event input",
            'expected_topics': {
                'slack_user_a':"I have a question about Packer",
                'slack_user_b':"I have an issue with Terraform ASG I would like to debug"
            }
        }
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))

    return response
