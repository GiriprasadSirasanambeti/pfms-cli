import mysql.connector

# Function to Establish Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

# Function to get total income and expenses
def get_income_expense(user_id):
    conn=get_db_connection()
    try:
        cursor=conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = %s AND type = 'Income'",(user_id,))
        total_income=cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = %s AND type = 'Expense'",(user_id,))
        total_expense=cursor.fetchone()[0] or 0
        return total_income, total_expense
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
        return 0, 0
    finally:
        cursor.close()
        conn.close()

# Function to get budget status
def get_budget_status():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT category, amount FROM budgets")
        budgets=cursor.fetchall()
        status_list=[]
        for category, budget_amount in budgets:
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE category =  %s AND type = 'Expense'",(category,))
            spent=cursor.fetchone()[0] or 0
            remaining = budget_amount -  spent
            status = "✅ Within Budget" if remaining >= 0 else "⚠️ Over Budget!"
            status_list.append(f"📂 {category}: 💰 Budget ₹{budget_amount} | 🛒 Spent ₹{spent} | 🔄 Remaining ₹{remaining} | {status}")
        return status_list
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


# Function to get last 5 transactions
def get_recent_transactions(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT amount, category, type, date FROM transactions WHERE user_id = %s ORDER BY date DESC LIMIT 5",(user_id,))
        transactions=cursor.fetchall()
        return transactions
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Function to display the user dashboard
def show_dashboard(user_id):
    print("\n 📊 ==== USER FINANCIAL DASHBOARD =====")

    # Get total income & expenses
    total_income, total_expense = get_income_expense(user_id)
    print(f"💰 Total Income: ₹{total_income}")
    print(f"🛒 Total Expenses: ₹{total_expense}")
    print(f"💾 Net Savings: ₹{total_income - total_expense}\n")

    #show budget status
    print("📂 Budget Overview:")
    budget_status=get_budget_status()
    for status in budget_status:
        print(status)
    print("\n")

    #Show recent transactions
    print("🔄 Recent Transactions:")
    recent_transactions = get_recent_transactions(user_id)
    for t in recent_transactions:
        print(f"💰 {t[0]} | 📂 {t[1]} | 🔄 {t[2]} | 📅 {t[3]}")

#Run the dashboard
if __name__=="__main__":
    user_id=1
    show_dashboard(user_id)