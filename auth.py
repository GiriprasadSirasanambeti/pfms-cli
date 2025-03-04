from decimal import Decimal
import mysql.connector
from mysql.connector import Error
import bcrypt

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="finance_db"
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

class User:
    def __init__(self, username, password=None, user_id=None):
        self.username = username
        self.password = password  # Plaintext initially, hashed on signup
        self.user_id = user_id

    def signup(self):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username=%s", (self.username,))
                if cursor.fetchone():
                    print("❌ Username Already Exists! Choose a Different One!")
                    return False
                self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (self.username, self.password))
                conn.commit()
                cursor.execute("SELECT id FROM users WHERE username=%s", (self.username,))
                self.user_id = cursor.fetchone()[0]
                print("✅ Signup successful!")
                return self.user_id
            except Error as e:
                print(f"Error: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
        return False

    def login(self, password):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, password FROM users WHERE username=%s", (self.username,))
                result = cursor.fetchone()
                if result:
                    self.user_id, stored_password = result
                    if bcrypt.checkpw(password.encode(), stored_password.encode()):
                        print("✅ Login Successful! Welcome,", self.username)
                        return self.user_id
                    else:
                        print("❌ Invalid Password!")
                        return False
                else:
                    print("❌ Username Not Found!")
                    return False
            except Error as e:
                print(f"Error: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
        return False

    def __str__(self):
        return f"User: {self.username} (ID: {self.user_id})"

# CLI compatibility functions
def signup(username, password):
    user = User(username, password)
    return user.signup()

def login(username, password):
    user = User(username)
    return user.login(password)

if __name__ == "__main__":
    user_id = signup("test_user", "password123")
    if user_id:
        print(f"User ID: {user_id}")
    user_id = login("test_user", "password123")
    if user_id:
        print(f"Logged in User ID: {user_id}")