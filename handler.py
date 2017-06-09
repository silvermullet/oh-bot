import boto3
import time
import decimal


client = boto3.client('dynamodb')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
table = dynamodb.Table('OfficeHoursBot')
today = time.strftime("%d/%m/%Y")

def create_dynamodb_table:
    table = dynamodb.create_table(
        TableName='OfficeHoursBot',
        KeySchema=[
            {
                'AttributeName': 'date',
                'KeyType': 'STRING'  #Partition key
            },
            {
                'AttributeName': 'location',
                'KeyType': 'STRING'  #Sort key
            }
            ],
        AttributeDefinitions=[
            {
                'AttributeName': 'date',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'location',
                'AttributeType': 'S'
            },

            ],
        ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
    )

    print("Table status:", table.table_status)

def set_office_hours(event, context):
    print(event)

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
