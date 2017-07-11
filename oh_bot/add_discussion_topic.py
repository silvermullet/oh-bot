import logging
import time

import boto3

dynamodb = boto3.client('dynamodb')

def add_discussion_topic(event, context):
    #debug print for lex event data
    print(event)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_TOPICS'])
    team     = event['currentIntent']['slots']['GetTeam']
    date     = event['currentIntent']['slots']['GetDay']

    response = table.update_item(
        Key={
            'team': team,
            'date': date
        },
        ExpressionAttributeNames={
            "#slack_user": event['slack_user'] ,
        },
        ExpressionAttributeValues = {
            ":string" : event['topic']
        },
        ConditionExpression = "attribute_not_exists(map.#slack_user)",
        UpdateExpression = "SET map.#slack_user = :string"
    )

    print("PutItem succeeded:")
    print(json.dumps(response['Attributes'], cls=DecimalEncoder))

    return response
