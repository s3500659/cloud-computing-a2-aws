import unittest
from dynamo_db import DynamoDbManager
import pprint


class UnitTest(unittest.TestCase):

    def setUp(self):
        self.client = DynamoDbManager()

        self.valid_email = 's35006590@student.rmit.edu.au'
        self.valid_pw = '012345'

        self.invalid_email = 'noone@student.rmit.edu.au'
        self.invalid_pw = 'abc123'
    
    def test_create_subscriptions(self):
        user = self.client.get_user('vinh')
        songs = self.client.query_music_item(
            artist="The Lumineers", title="", year="")
        
        self.assertTrue(songs)

        for song in songs:
            self.client.subscribe_music(user, song)


    def test_subscribe_music(self):
        user = self.client.get_user(self.valid_email)

        # add song 1
        song_1 = self.client.query_music_item(
            artist="Arcade Fire", title="Half Light I", year="2010")

        self.client.subscribe_music(user, song_1[0])

        self.assertTrue(self.client.get_subscription(
            user['email'], song_1[0]))
        # add song 2
        song_2 = self.client.query_music_item(
            artist="", title="Lean On Me", year="")

        self.client.subscribe_music(user, song_2[0])
        self.assertTrue(self.client.get_subscription(
            user['email'], song_2[0]))

        # check both song exist
        self.assertTrue(self.client.get_subscriptions(user['email']))

        # delete songs
        self.client.delete_subscription(user['email'], song_1[0]['title'])
        self.client.delete_subscription(user['email'], song_2[0]['title'])

        self.assertFalse(
            self.client.get_subscription(user['email'], song_1[0]))
        self.assertFalse(
            self.client.get_subscription(user['email'], song_2[0]))

        # invalid email
        self.assertFalse(
            self.client.get_subscriptions(self.invalid_email))

    def test_get_music_item(self):
        # full query
        self.assertTrue(self.client.query_music_item(
            artist="Arcade Fire", title="Half Light I", year="2010"))
        # one item missing
        self.assertTrue(self.client.query_music_item(
            artist="", title="Half Light I", year="2010"))

        self.assertTrue(self.client.query_music_item(
            artist="Arcade Fire", title="", year="2010"))

        self.assertTrue(self.client.query_music_item(
            artist="Arcade Fire", title="Half Light I", year=""))

        # two item missing
        self.assertTrue(self.client.query_music_item(
            artist="", title="", year="2010"))

        self.assertTrue(self.client.query_music_item(
            artist="Arcade Fire", title="", year=""))

        self.assertTrue(self.client.query_music_item(
            artist="", title="Half Light I", year=""))

        # all items missing
        self.assertFalse(self.client.query_music_item(
            artist="", title="", year=""))

        # mismatch query
        self.assertFalse(self.client.query_music_item(
            artist="Arcade Fire", title="Lean On Me", year="1970"))

    def test_get_user(self):
        self.assertIsNotNone(self.client.get_user(self.valid_email))
        self.assertIsNone(self.client.get_user(self.invalid_email))

    def test_create_user(self):
        email = 'test@student.rmit.edu.au'
        user_name = 'test_user'
        pw = '123'
        self.client.create_user(email, user_name, pw)
        self.assertIsNotNone(self.client.get_user(email))
        self.client.delete_user(email)
        self.assertIsNone(self.client.get_user(email))


if __name__ == '__main__':
    unittest.main()
