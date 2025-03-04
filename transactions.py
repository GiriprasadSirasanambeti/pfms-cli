import mysql.connector
from datetime import datetime
from budget import check_budget
from decimal import Decimal

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

class Transaction:
    def __init__(self, user_id, amount, category, type, date = None):
        self.user_id = user_id
        self.amount = Decimal(str(amount))
        self.category = category
        self.type = type.capitalize()
        self.date = date or datetime.now()

    def add(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            if self.type.lower() == "expense":
                if not check_budget(cursor, self.category, self.amount):
                    print(f"⚠️ Warning: Adding ₹{self.amount} to {self.category} exceeds the Budget!")
                    return
            query = """
            INSERT INTO transactions (user_id, amount, category, type, date)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.user_id, self.amount, self.category, self.type, self.date))
            conn.commit()
            print(f"✅ Transaction Added successfully: {self.amount} ({self.type}) in {self.category}")
        except mysql.connector.Error as e:
            print(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def __str__(self):
        return f"{self.type}: {self.amount} in {self.category} on {self.date}"

# Function to Add a Transaction (Income/Expense)
def add_transaction(user_id,amount,category,type):
    trans = Transaction(user_id, amount, category, type)
    trans.add()

#Function to View All Transactions for a User
def view_transactions(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        #fetches all transactions of a user
        query="SELECT id, amount, category, type, date FROM transactions WHERE user_id = %s ORDER BY date DESC"
        cursor.execute(query,(user_id,))
        transactions=cursor.fetchall()

        if transactions:
            print("\n 📊 Your Transactions:")
            for t in transactions:
                print(f"🆔 {t[0]} | 💰 {t[1]} | 📂 {t[2]} | 🔄 {t[3]} | 📅 {t[4]}")
        else:
            print("⚠️ No transactions found!")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to Delete a Transaction by ID
def delete_transaction(transaction_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        #delete a transaction by id
        query="DELETE FROM transactions WHERE id = %s"
        cursor.execute(query,(transaction_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Transaction {transaction_id} deleted successfully!")
        else:
            print(f"⚠️ Transaction {transaction_id} Not Found !")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Example (You can comment these out later)
if __name__=="__main__":
    user_id=1

    # Example: Add a Transaction
   # add_transaction(user_id, 50000, "Salary", "Income")
    add_transaction(user_id, 2000,"Grocery", "Expense")

    # Example: View Transactions
    view_transactions(user_id)

    # Example: Delete a Transaction
    delete_transaction(1)

