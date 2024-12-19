import unittest
from user import create_user, authenticate_user
from database import setup_database

class TestFinanceApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup_database()  # Set up the database for testing

    def test_user_creation(self):
        create_user("testuser", "password123")
        self.assertIsNotNone(authenticate_user("testuser", "password123"))

    def test_authentication_fail(self):
        self.assertIsNone(authenticate_user("testuser", "wrongpassword"))

if __name__ == '__main__':
    unittest.main()
