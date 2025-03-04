import csv
import mysql.connector

# Establish Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

#Export Transaction to CSV
def export_transactions_to_csv(user_id, filename = "transactions_export.csv"):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        query = "SELECT id, amount, category, type, date FROM transactions WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        transactions = cursor.fetchall()

        if transactions:
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Transaction ID", "Amount", "Category", "Type", "Date"])
                writer.writerows(transactions)
            print(f"✅ Transactions exported successfully to {filename}!")
        else:
            print("❌ No Transactions Found to Export.")
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Import Transactions from CSV
def import_transactions_from_csv(user_id, filename = "transactions_import.csv"):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                transaction_id, amount, category, trans_type, date = row
                query = """
                INSERT INTO transactions (id, user_id, amount, category, type, date)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE amount=VALUES(amount), category=VALUES(category), date=VALUES(date)
                """
                cursor.execute(query, (transaction_id, user_id, amount, category, trans_type, date))
        conn.commit()
        print(f"✅ Transactions Imported successfully from {filename}!")
    except Exception as e:
        print(f"❌ Error importing transactions: {e}")

    cursor.close()
    conn.close()

#example usage
if __name__=="__main__":
    user_id = 1
    export_transactions_to_csv(user_id)
    import_transactions_from_csv(user_id)
