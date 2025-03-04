from decimal import Decimal
import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

def set_budget(category, amount):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = """ 
        INSERT INTO budgets (category, amount) 
        VALUES (%s, %s) 
        ON DUPLICATE KEY UPDATE amount = %s
        """
        cursor.execute(query, (category, amount, amount))
        conn.commit()
        print(f"✅ Budget Set: {category} -> ₹{amount}")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

def view_budget():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT category, amount FROM budgets"
        cursor.execute(query)
        budgets = cursor.fetchall()
        print("\n 📊 Your Budgets:")
        for category, amount in budgets:
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE category = %s AND type = 'expense'", (category,))
            spent = cursor.fetchone()[0] or 0
            remaining = amount - spent
            status = "✅ Within Budget" if remaining >= 0 else "⚠️ Over Budget!"
            print(f"📂 {category}: 💰 Budget ₹{amount} | 🛒 Spent ₹{spent} | 🔄 Remaining ₹{remaining} | {status}")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

def check_budget(cursor, category, expense):
    try:
        query = "SELECT amount FROM budgets WHERE category = %s"
        cursor.execute(query, (category,))
        budget = cursor.fetchone()
        if budget:
            budget_amount = Decimal(str(budget[0]))
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE category = %s AND type = 'expense'", (category,))
            total_spent = Decimal(str(cursor.fetchone()[0] or 0))
            expense = Decimal(str(expense))
            if total_spent + expense > budget_amount:
                print(f"⚠️ Warning! Budget Exceeded for {category}. Spent: ₹{total_spent + expense}, Budget: ₹{budget_amount}")
                return False
        else:
            print(f"⚠️ No Budget Set For {category}. Consider Setting One.")
        return True
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
        return True

if __name__ == "__main__":
    set_budget("Grocery", 5000)
    set_budget("Entertainment", 3000)
    view_budget()