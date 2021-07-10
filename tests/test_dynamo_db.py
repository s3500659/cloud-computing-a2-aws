from dynamo_db import dynamo_db
import unittest


class TestDynamoDb(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setUpClass')

    def setUp(self):
        self.client = dynamo_db()

    def tearDown(self):
        pass

    def test_get_user(self):
        valid_email = 's35006590@student.rmit.edu.au'
        invalid_email = 'noone@student.rmit.edu.au'

        self.assertIsNotNone(self.client.get_user(valid_email))
        self.assertIsNone(self.client.get_user(invalid_email))

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
