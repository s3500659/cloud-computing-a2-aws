import boto3
import json
from boto3.dynamodb.conditions import Attr


class DynamoDbManager:

    def __init__(self):
        self.__dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.__client = boto3.client('dynamodb', region_name='us-east-1')
        self.MUSIC_SUB_TABLE = 'user_subscription'

        # self.__dynamodb = boto3.resource(
        #     'dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')
        # self.__client = boto3.client(
        #     'dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')

    def delete_subscription(self, email, title):
        table = self.__dynamodb.Table(self.MUSIC_SUB_TABLE)

        table.delete_item(
            Key={
                'email': email,
                'title': title
            }
        )

    def get_subscriptions(self, email):
        table = self.__dynamodb.Table(self.MUSIC_SUB_TABLE)

        response = table.scan(
            FilterExpression=Attr('email').eq(email)
        )

        items = response['Items']

        return items

    def get_subscription(self, email, song):
        table = self.__dynamodb.Table(self.MUSIC_SUB_TABLE)

        response = table.scan(
            FilterExpression=Attr('email').eq(
                email) & Attr('title').eq(song['title'])
        )

        items = response['Items']

        return items

    def subscribe_music(self, user, song):
        if self.table_exist(self.MUSIC_SUB_TABLE) == False:
            self.create_table_double(
                self.MUSIC_SUB_TABLE, 'email', 'S', 'title', 'S')

        table = self.__dynamodb.Table(self.MUSIC_SUB_TABLE)

        table.put_item(
            Item={
                'email': user['email'],
                'title': song['title'],
                'artist': song['artist'],
                'year': song['year']
            }
        )

    def query_music_item(self, artist="", title="", year=""):
        table = self.__dynamodb.Table('music')

        # complete query
        if artist != "" and title != "" and year != "":
            response = table.scan(
                FilterExpression=Attr('artist').eq(artist) & Attr(
                    'title').eq(title) & Attr('year').eq(year)
            )
        # one attr missing
        if artist == "" and title != "" and year != "":
            response = table.scan(
                FilterExpression=Attr('title')
                .eq(title) & Attr('year').eq(year)
            )
        if artist != "" and title == "" and year != "":
            response = table.scan(
                FilterExpression=Attr(
                    'artist').eq(artist) & Attr('year').eq(year)
            )
        if artist != "" and title != "" and year == "":
            response = table.scan(
                FilterExpression=Attr(
                    'artist').eq(artist) & Attr('title').eq(title)
            )
        # two attr missing
        if artist == "" and title == "" and year != "":
            response = table.scan(
                FilterExpression=Attr('year').eq(year)
            )
        if artist == "" and title != "" and year == "":
            response = table.scan(
                FilterExpression=Attr('title').eq(title)
            )
        if artist != "" and title == "" and year == "":
            response = table.scan(
                FilterExpression=Attr('artist').eq(artist)
            )
        # empty query
        if artist == "" and title == "" and year == "":
            response = table.scan(
                FilterExpression=Attr('artist').eq(artist) & Attr(
                    'title').eq(title) & Attr('year').eq(year)
            )

        items = response['Items']

        return items

    def delete_user(self, email):
        table = self.__dynamodb.Table('login')
        table.delete_item(
            Key={'email': email}
        )

    def create_user(self, email, user_name, password):
        table = self.__dynamodb.Table('login')

        table.put_item(
            Item={
                'email': email,
                'user_name': user_name,
                'password': password
            }
        )

    def scan_table(self, table_name, attr, user_name):
        table = self.__dynamodb.Table(table_name)

        response = table.scan(
            FilterExpression=Attr(attr).eq(user_name)
        )
        try:
            items = response['Items']
        except:
            return None

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

    def create_login_table(self):
        table_name = 'login'
        print(f"Creating {table_name} table...")
        table = self.__dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    def create_table_single(self, table_name, p_key, p_type):
        print(f"Creating {table_name} table...")
        table = self.__dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': p_key,
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': p_key,
                    'AttributeType': p_type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    def create_table_double(self, table_name, p_key, p_type, s_key, s_type):
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
