import json
import unittest
from moto import mock_dynamodb2
import boto3
from handler import create_employee, get_employee, update_employee, delete_employee

# Set up the mock DynamoDB service
@mock_dynamodb2
def setup_dynamodb():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    dynamodb.create_table(
        TableName='employeeTable',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'N'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    return dynamodb


class TestHandler(unittest.TestCase):
    def setUp(self):
        self.dynamodb = setup_dynamodb()

    def test_create_employee(self):
        event = {
            'body': '{"id": 1, "name": "John Doe", "age": 30}'
        }
        response = create_employee(event, {})
        self.assertEqual(response['statusCode'], 200)

        # Check if the item was inserted correctly
        table = self.dynamodb.Table('employeeTable')
        item = table.get_item(Key={'id': 1})['Item']
        self.assertEqual(item['name'], 'John Doe')
        self.assertEqual(item['age'], 30)

    def test_get_employee(self):
        # Insert a sample item
        table = self.dynamodb.Table('employeeTable')
        table.put_item(Item={'id': 1, 'name': 'John Doe', 'age': 30})

        event = {
            'pathParameters': {'id': '1'}
        }
        response = get_employee(event, {})
        self.assertEqual(response['statusCode'], 200)

        body = json.loads(response['body'])
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['name'], 'John Doe')
        self.assertEqual(body['age'], 30)

    def test_update_employee(self):
        # Insert a sample item
        table = self.dynamodb.Table('employeeTable')
        table.put_item(Item={'id': 1, 'name': 'John Doe', 'age': 30})

        event = {
            'pathParameters': {'id': '1'},
            'body': '{"name": "Jane Doe", "age": 35}'
        }
        response = update_employee(event, {})
        self.assertEqual(response['statusCode'], 200)

        # Check if the item was updated correctly
        item = table.get_item(Key={'id': 1})['Item']
        self.assertEqual(item['name'], 'Jane Doe')
        self.assertEqual(item['age'], 35)

    def test_delete_employee(self):
        # Insert a sample item
        table = self.dynamodb.Table('employeeTable')
        table.put_item(Item={'id': 1, 'name': 'John Doe', 'age': 30})

        event = {
            'pathParameters': {'id': '1'}
        }
        response = delete_employee(event, {})
        self.assertEqual(response['statusCode'], 200)

        # Check if the item was deleted
        with self.assertRaises(table.meta.client.exceptions.ResourceNotFoundException):
            table.get_item(Key={'id': 1})

