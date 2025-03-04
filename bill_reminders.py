from decimal import Decimal
import mysql.connector
from datetime import datetime, timedelta, date  # Added 'date' import
from transactions import Transaction, get_db_connection

class RecurringBill:
    def __init__(self, user_id, category, amount, due_date, frequency, bill_id=None):
        self.user_id = user_id
        self.category = category
        self.amount = Decimal(str(amount))
        self.due_date = due_date if isinstance(due_date, date) else datetime.strptime(due_date, "%Y-%m-%d").date()
        self.frequency = frequency
        self.bill_id = bill_id

    def add(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM recurring_bills 
                WHERE user_id = %s AND category = %s AND amount = %s AND due_date = %s AND frequency = %s
            """, (self.user_id, self.category, self.amount, self.due_date, self.frequency))
            if cursor.fetchone():
                print(f"⚠️ Recurring Bill Already Exists: {self.category} - ₹{self.amount}, Due Date: {self.due_date}")
            else:
                query = """
                INSERT INTO recurring_bills (user_id, category, amount, due_date, frequency)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (self.user_id, self.category, self.amount, self.due_date, self.frequency))
                conn.commit()
                print(f"✅ Recurring Bill Added: {self.category} - ₹{self.amount}, Due Date: {self.due_date}, Frequency: {self.frequency}")
        except mysql.connector.Error as e:
            print(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def __str__(self):
        return f"Bill: {self.category} - ₹{self.amount}, Due: {self.due_date}, Frequency: {self.frequency}"

def add_recurring_bill(user_id, category, amount, due_date, frequency):
    bill = RecurringBill(user_id, category, amount, due_date, frequency)
    bill.add()

def view_recurring_bills(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT id, category, amount, due_date, frequency FROM recurring_bills WHERE user_id = %s ORDER BY due_date"
        cursor.execute(query, (user_id,))
        bills = cursor.fetchall()
        if bills:
            print("\n 📆 Your Recurring Bills:")
            for bill in bills:
                print(f"🆔{bill[0]} | 📂 {bill[1]} | 💰 ₹{bill[2]} | 📅 Due: {bill[3]} | 🔄{bill[4].capitalize()}")
        else:
            print("⚠️ No Recurring Bills Found!")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

def check_and_process_bills(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        today = datetime.today().date()
        query = "SELECT id, category, amount, due_date, frequency FROM recurring_bills WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        bills = cursor.fetchall()
        if not bills:
            print("✅ No recurring bills to process.") 
            return
        processed = False
        for bill in bills:
            bill_id, category, amount, due_date, frequency = bill
            if due_date <= today:
                print(f"📌 Processing Due Bill: {category} - ₹{amount}")
                trans = Transaction(user_id, amount, category, "Expense")
                trans.add()
                next_due_date = due_date + timedelta(days=30 if frequency.lower() == "monthly" else 7)
                update_query = "UPDATE recurring_bills SET due_date = %s WHERE id = %s"
                cursor.execute(update_query, (next_due_date, bill_id))
                conn.commit()
                print(f"🔄 Next Due Date updated: {next_due_date}")
                processed = True
        if not processed:
            print("✅ No bills due today.")  # Added for clarity
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    user_id = 1
    add_recurring_bill(user_id, "Electricity", 1200, "2025-03-03", "monthly")
    view_recurring_bills(user_id)
    check_and_process_bills(user_id)