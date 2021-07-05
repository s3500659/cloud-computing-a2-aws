import boto3
from botocore.exceptions import ClientError


class dynamo_db:

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.client = boto3.client('dynamodb')

    def get_table(self, table_name):
        return self.dynamodb.Table(table_name)

    def load_music_data(self, json_file):
        table = self.dynamodb.Table('music')
        print("Loading music data...")
        for item in json_file['songs']:
            table.put_item(Item=item)

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
