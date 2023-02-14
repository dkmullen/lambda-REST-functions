import json
from datetime import datetime
import uuid
import boto3
import helpers

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    id = str(uuid.uuid4())
    created = str(datetime.now())
    method = event['httpMethod']
    
    obj=json.loads(event['body'])
    obj['id'] = id
    obj['created'] = created
    obj_formatted = helpers.dict_to_item(obj)


    def putItem():
        response = client.put_item(
            Item = obj_formatted,
            TableName='restApiTable',
        )
        if response:
            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps({
                    'message': 'Document id: ' + id,
                    'data': response
                })
            }

            
    def getItem():
        req = json.loads(event['body'])
        id = req['id']
        response = client.get_item(
            Key={
                'id': {
                    'S': req['id'],
                    },
                'category': {
                    'S': req['category'],
                },

            },
            TableName='restApiTable',
        )
        if response:
            res = json.dumps(response)
            return {
                'statusCode': 200,
                'body': res
            }

    
        
    if method == 'POST' or method == 'PUT':
        return putItem()
    elif method == 'GET':
        return getItem()
