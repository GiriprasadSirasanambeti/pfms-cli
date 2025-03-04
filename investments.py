import mysql.connector
from decimal import Decimal



#Establish Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

# Add a New Investment
def add_investment(user_id, investment_name, amount, investment_type, purchase_date, return_rate=0.00):
    conn=get_db_connection()
    try:
        cursor=conn.cursor()

        # Convert values to correct types
        amount = Decimal(amount)
        return_rate = Decimal(return_rate)
        # Check if the investment already exists for the user
        query_check = "SELECT id FROM investments WHERE user_id = %s AND investment_name = %s"
        cursor.execute(query_check, (user_id, investment_name))
        existing = cursor.fetchone()
        if existing:
            print(f"‼️ Investment '{investment_name}' already exists! Duplicate investments are not allowed.")
        else:
            query_insert = """
            INSERT INTO investments (user_id, investment_name, amount, investment_type, purchase_date, return_rate, current_value)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert, (user_id, investment_name, amount, investment_type, purchase_date, return_rate, amount))
            conn.commit()
            print(f"✅ Investment '{investment_name}' Added Successfully!")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# View Investments
def view_investments(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        query = "SELECT id, investment_name, amount, investment_type, purchase_date, return_rate, current_value FROM investments WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        investments = cursor.fetchall()

        if investments:
            print("\n 📊 Your Investments:")
            for inv in investments:
                inv_id, name, amount, inv_type, date, return_rate, value = inv
                date = date.strftime("%Y-%m-%d")   # Convert datetime to string
                print(f"🆔 {inv_id} | {name} | 💰 Invested: ₹{amount} | 📅 Date: {date} | 📈 Type: {inv_type} | 📊 Return rate: {return_rate}% | 💴 Current Value: ₹{value}")
        else:
            print("❌ No Investments Found!")
    except mysql.connector.Error as e:
            print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

#Delete an Investment
def delete_investment(investment_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        query_delete = "DELETE FROM investments WHERE id = %s"
        cursor.execute(query_delete, (investment_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ Investment ID {investment_id} deleted successfully!")
        else:
            print(f"❌ Investment ID {investment_id} Not Found!")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

#Sample Usage
if __name__=="__main__":
    user_id = 1

    add_investment(user_id, "Tesla Stock", 100000, "Stock", "2025-02-28",10.5)
    add_investment(user_id, "Motilal Oswal Midcap-Fund", 2500, "Mutual Funds","2024-12-04", 3.0)
    view_investments(user_id)
    delete_investment(0)