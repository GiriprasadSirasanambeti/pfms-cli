import mysql.connector
from datetime import datetime, timedelta

# Establish Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

# Fetch Upcoming Bills
def check_due_bills(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        today = datetime.today().date()
        upcoming_due_date = today + timedelta(days=3)

        query = "SELECT category, due_date, amount FROM recurring_bills WHERE user_id = %s AND due_date <= %s"
        params = (user_id, upcoming_due_date)  # ✅ Ensure tuple format
        cursor.execute(query, params)
        bills = cursor.fetchall()
        if bills:
            print("\n📢 *** Upcoming Bill Reminders: ***")
            for bill in bills:
                name, due_date, amount = bill
                print(f" 🔔 {name} - Due On {due_date} | Amount ₹{amount}")
        else:
            print("✅ No upcoming bills in the next 3 days.")
    except mysql.connector.Error as e:
            print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Low Balance Notification
def check_low_balance(user_id, threshold=1000):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        query = "SELECT balance FROM accounts WHERE id = %s"
        cursor.execute(query,(user_id,))
        balance = cursor.fetchone()
        if balance and balance[0] < threshold:
            print(f"⚠️ Warning! Your account balance is low! ₹{balance[0]} remaining.")
        else:
            print("✅ Your account balance is good.")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Goal Deadline Notifications
def check_goal_deadlines(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        today = datetime.today().date()
        upcoming_goal_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")  # Convert to string
        query = "SELECT goal_name, target_amount, saved_amount, deadline FROM goals WHERE user_id = %s AND deadline <= %s"
        params =(user_id,upcoming_goal_date)   #ensure tuple format
        cursor.execute(query, params)
        goals = cursor.fetchall()
        if goals:
            print("\n🎯 **Goal Deadline Reminders:**")
            for goal in goals:
                name, target, saved, deadline = goal
                print(f"📌 {name} - Target: ₹{target}, Saved: ₹{saved} | Deadline: {deadline}")
        else:
            print("✅ No goals reaching deadlines soon.")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Run Notifications
if __name__=="__main__":
    user_id=1

    print("\n🔔 **Notifications & Alerts** 🔔")
    check_due_bills(user_id)
    check_low_balance(user_id, threshold=2000)
    check_goal_deadlines(user_id)