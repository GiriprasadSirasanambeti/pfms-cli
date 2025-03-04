import mysql.connector
from tabulate import tabulate

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

# Function to categorize expenses
def categorize_expense(transaction_id, category_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Check if the transaction exists
        cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
        transaction = cursor.fetchone()
        if not transaction:
            print(f"❌ Transaction ID {transaction_id} Not Found")
            return
        query = """
        INSERT INTO categorized_expenses (transaction_id, category_id)
        VALUES (%s, %s)
        """
        cursor.execute(query, (transaction_id, category_id,))
        conn.commit()
        print(f"✅ Transaction ID {transaction_id} Categorized Successfully!")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to display spending insights
def show_spending_insights(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = """
        SELECT ec.category_name, SUM(t.amount) AS total_spent
        FROM categorized_expenses ce
        JOIN transactions t ON ce.transaction_id = t.id
        JOIN expense_categories ec ON ce.category_id = ec.category_id
        WHERE t.user_id = %s AND t.type = 'expense'
        GROUP BY ec.category_name
        ORDER BY total_spent DESC
        """

        cursor.execute(query, (user_id,))
        insights = cursor.fetchall()

        if not insights:
            print("ℹ️ No spending insights available.")
            return
        else:
            print("\n Spending Insights:")
            print(tabulate(insights, headers=["Category", "Total Spent"], tablefmt="grid"))
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()
#Example usage
if __name__=="__main__":
    user_id=1
    categorize_expense(2,3)
    show_spending_insights(user_id)
