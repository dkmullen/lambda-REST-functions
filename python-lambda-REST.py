import boto3 
import json 
import uuid 
import datetime 
import helpers
import os

from boto3.dynamodb.types import TypeDeserializer 

deser = TypeDeserializer() 
resource = boto3.resource('dynamodb') 
client = boto3.client('dynamodb') 
tableName = os.environ['TABLENAME']
table = resource.Table(tableName) 
headers = { 
    'Access-Control-Allow-Headers': 'Content-Type', 
    'Access-Control-Allow-Origin': os.environ['AccessControlAllowOrigin'], 
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE' 
} 

def lambda_handler(event, context): 
    def saveItem(): 
        params = json.loads(event['body']) 
        try: 
            params['id'] = str(uuid.uuid4()) 
            params['created'] = str(datetime.datetime.now()) 
            response = table.put_item(Item=params) 
            if response: 
                return { 
                    'statusCode': response['ResponseMetadata']['HTTPStatusCode'], 
                    'headers': headers, 
                    'body': json.dumps({ 
                        'message': 'Document id: ' + params['id'], 
                        'data': response 
                    }) 
                } 

        except: 
            return { 
                'statusCode': 500, 
                'headers': headers, 
                'body': json.dumps('An error occurred') 
            } 

  
    def getItem(): 
        params = event['queryStringParameters'] 
        if params['id'] == 'GETALL': 
            return scan() 
        else: 
            try: 
                response = client.get_item( 
                    TableName=tableName, 
                    Key={ 
                        'id': { 
                            'S': params['id'], 
                        }, 
                        'category': { 
                            'S': params['category'] 
                        } 
                    } 
                ) 

                if response: 
                    item = response['Item'] 
                    deserialized = {} 
                    for key in item: 
                        deserialized[key] = deser.deserialize(item[key]) 

                    return { 
                        'statusCode': 200, 
                        'headers': headers, 
                        'body': json.dumps(deserialized) 
                    } 

            except: 
                return { 
                    'statusCode': 500, 
                    'headers': headers, 
                    'body': json.dumps('An error occurred') 
                } 

    def scan(): 
        try: 
            response = client.scan(TableName=tableName) 
            deserialized_list = [] 
            for i in response['Items']: 
                deserialized_dict = {} 
                for key in i: 
                    deserialized_dict[key] = deser.deserialize(i[key]) 

                deserialized_list.append(deserialized_dict) 

            if response: 
                return { 
                    'statusCode': 200, 
                    'headers': headers, 
                    'body': json.dumps(deserialized_list) 
                } 

        except: 
            return { 
                'statusCode': 500, 
                'headers': headers, 
                'body': json.dumps('An error occurred') 
            } 
  

    def updateItem(): 
        params = json.loads(event['body']) 
        try: 
            response = table.put_item(Item=params) 
            if response: 
                return { 
                    'statusCode': response['ResponseMetadata']['HTTPStatusCode'], 
                    'headers': headers, 
                    'body': json.dumps({ 
                        'message': 'Document id: ' + params['id'], 
                        'data': response 
                    }) 
                } 

        except: 
            return { 
                'statusCode': 500, 
                'headers': headers, 
                'body': json.dumps('An error occurred') 
            } 

        return { 
            'statusCode': 200, 
            'headers': headers, 
            'body': json.dumps(params) 
        } 

  
    def deleteItem(): 
        params = json.loads(event['body']) 
        try: 
            response = client.delete_item( 
                TableName=tableName, 
                Key={ 
                    'id': { 
                        'S': params['id'], 
                    }, 
                    'category': { 
                        'S': params['category'] 
                    } 
                } 
            ) 

            if response: 
                return { 
                    'statusCode': 200, 
                    'headers': headers, 
                    'body': json.dumps('Deleted') 
                } 

        except: 
            return { 
                'statusCode': 500, 
                'headers': headers, 
                'body': json.dumps('An error occurred, dangit') 
            } 


    if event['httpMethod'] == 'POST': 
        return saveItem()

    elif event['httpMethod'] == 'GET': 
        return getItem() 

    elif event['httpMethod'] == 'PUT': 
        return updateItem() 

    elif event['httpMethod'] == 'DELETE': 
        return deleteItem() 

 