import mysql.connector
from datetime import datetime

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )
# ✅ Function to Get Monthly Expense Summary
def monthly_expenses_summary(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        """ Shows total expense per month for a user. """
        query="""
        SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount)
        FROM transactions
        WHERE user_id = %s AND type='Expense'
        GROUP BY month
        ORDER BY month DESC
        """
        cursor.execute(query, (user_id,))
        results=cursor.fetchall()

        print("\n📊 Monthly Expense Summary:")
        for row in results:
            print(f"📅 {row[0]} | 💰 {row[1]}")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ Function to Get Category-wise Expense Summary
def category_expense_summary(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        """ Shows spending breakdown by category. """
        query="""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_id = %s AND type = 'Expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
        """

        cursor.execute(query,(user_id,))
        results=cursor.fetchall()

        print("\n📂 Category-wise Expense Summary:")
        for row in results:
            print(f"📂 {row[0]} | 💸 {row[1]}")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ Function to Compare Income vs Expense
def income_vs_expense(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        """ Shows total income vs total expense. """
        query="""
        SELECT type, SUM(amount)
        FROM transactions
        WHERE user_id = %s
        GROUP BY type
        """
        cursor.execute(query,(user_id,))
        results=cursor.fetchall()

        print("\n💰 Income vs Expense:")
        for row in results:
            print(f"🔄 {row[0]} | 💰 {row[1]}")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ Example Usage (Test this script)
if __name__=="__main__":
    user_id=1

    monthly_expenses_summary(user_id)
    category_expense_summary(user_id)
    income_vs_expense(user_id)

