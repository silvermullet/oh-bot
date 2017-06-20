import logging
import time
import decimal

from todos import decimalencoder
import boto3

dynamodb = boto3.client('dynamodb')

def get_date_topics(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'date': event['date']
            'slack_team': data['slack_team'],
            'slack_channel': data['slack_channel'],
        }
    )

    return json.dumps(result['Item']['expected_topics'], cls=decimalencoder.DecimalEncoder)

def add_discussion_topic(event, context):
    #debug print for lex event data
    print(event)

    data = json.loads(event['body'])

    if 'topic' not in data or 'date' not in data:
        logging.error("Validation Failed")
        raise Exception("Could not set office hours, need topic and date")
        return

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    today = time.strftime("%d/%m/%Y")

    response = table.update_item(
        Key={
            'date': event['date'],
            'slack_team': data['slack_team'],
            'slack_channel': data['slack_channel'],
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
