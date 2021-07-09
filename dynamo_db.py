import boto3
import json
from boto3.dynamodb.conditions import Key, Attr


class dynamo_db:

    def __init__(self):
        self.__dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.__client = boto3.client('dynamodb', region_name='us-east-1')

    def create_user(self, email, user_name, password):
        table = self.__dynamodb.Table('login')

        table.put_item(
            Item={
                'email': email,
                'user_name': user_name,
                'password': password
            }
        )
        print("User created...")

    def scan_table(self, table_name, attr, user_name):
        table = self.__dynamodb.Table(table_name)

        response = table.scan(
            FilterExpression=Attr(attr).eq(user_name)
        )
        try:
            items = response['Items']
        except:
            return None

        print(items)
        return items

    def get_user(self, user_email: str):
        table = self.__dynamodb.Table('login')

        response = table.get_item(
            Key={'email': user_email}
        )
        try:
            item = response['Item']
        except:
            return None

        return item

    def get_table(self, table_name):
        return self.__dynamodb.Table(table_name)

    def load_music_data(self, json_file):
        table = self.__dynamodb.Table('music')
        print("Loading music data...")

        with open(json_file) as json_data:
            music_data = json.load(json_data)

            for item in music_data['songs']:
                table.put_item(Item=item)

        print("Music data loaded...")

    def table_exist(self, table_name):
        tables = self.__client.list_tables()['TableNames']
        if table_name not in tables:
            return False

        return True

    def create_table(self, table_name, p_key, p_type, s_key, s_type):
        print(f"Creating {table_name} table...")
        table = self.__dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': p_key,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': s_key,
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': p_key,
                    'AttributeType': p_type
                },
                {
                    'AttributeName': s_key,
                    'AttributeType': s_type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
