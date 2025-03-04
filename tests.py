import unittest
from auth import User
from transactions import Transaction, get_db_connection

class TestPFMS(unittest.TestCase):
    def setUp(self):
        # Clear test data
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = 'testuser'")
        cursor.execute("DELETE FROM transactions WHERE category = 'Test'")
        conn.commit()
        cursor.close()
        conn.close()

    def test_signup(self):
        user = User("testuser", "pass123")
        user_id = user.signup()
        self.assertTrue(isinstance(user_id, int))
        self.assertEqual(user.username, "testuser")

    def test_login(self):
        user = User("testuser", "pass123")
        user.signup()
        user_id = user.login("pass123")
        self.assertTrue(user_id)
        self.assertFalse(user.login("wrongpass"))

    def test_add_transaction(self):
        user = User("testuser", "pass123")
        user_id = user.signup()
        trans = Transaction(user_id, 1000, "Test", "Income")
        trans.add()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE user_id=%s AND category='Test'", (user_id,))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

if __name__ == "__main__":
    unittest.main()