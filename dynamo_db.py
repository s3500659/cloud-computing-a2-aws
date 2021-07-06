import boto3
import json


class dynamo_db:

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.client = boto3.client('dynamodb')

    def get_user(self, user_email: str):
        table = self.dynamodb.Table('login')

        response = table.get_item(
            Key={'email': user_email}
        )
        try:
            item = response['Item']
        except:
            return None

        return item

    def get_table(self, table_name):
        return self.dynamodb.Table(table_name)

    def load_music_data(self, json_file):
        table = self.dynamodb.Table('music')
        print("Loading music data...")

        with open(json_file) as json_data:
            music_data = json.load(json_data)

            for item in music_data['songs']:
                table.put_item(Item=item)

        print("Music data loaded...")

    def table_exist(self, table_name):
        tables = self.client.list_tables()['TableNames']
        if table_name not in tables:
            return False

        return True

    def create_music_table(self):
        print("Creating music table...")
        table = self.dynamodb.create_table(
            TableName='music',
            KeySchema=[
                {
                    'AttributeName': 'title',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'artist',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'artist',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName='music')

        return table
