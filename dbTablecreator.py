from __future__ import print_function ## From AWS tutorials
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

table = dynamodb.create_table(
    TableName='Natural_Gas_Prices',
    KeySchema=[
        {
            'AttributeName': 'date',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'date',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 6000,
        'WriteCapacityUnits': 6000
    }
)

