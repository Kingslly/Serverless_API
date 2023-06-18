import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('employeeTable')


def create_employee(event, context):
    try:
        data = json.loads(event['body'])
        response = table.put_item(Item=data)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except ClientError as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }


def get_employee(event, context):
    try:
        employee_id = int(event['pathParameters']['id'])
        response = table.get_item(Key={'id': employee_id})
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    except (KeyError, ValueError, ClientError) as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }


def update_employee(event, context):
    try:
        employee_id = int(event['pathParameters']['id'])
        data = json.loads(event['body'])
        response = table.update_item(
            Key={'id': employee_id},
            UpdateExpression='SET #name = :name, #age = :age',
            ExpressionAttributeNames={
                '#name': 'name',
                '#age': 'age'
            },
            ExpressionAttributeValues={
                ':name': data['name'],
                ':age': data['age']
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except (KeyError, ValueError, ClientError) as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }


def delete_employee(event, context):
    try:
        employee_id = int(event['pathParameters']['id'])
        response = table.delete_item(Key={'id': employee_id})
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except (KeyError, ValueError, ClientError) as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }

