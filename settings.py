import mysql.connector
import bcrypt

# Establish Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

# Update Username
def update_username(user_id, new_username):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "UPDATE users SET username = %s WHERE id =%s"
        cursor.execute(query, (new_username, user_id))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Username updated successfully to '{new_username}'!")
        else:
            print("❌ No changes made. Please check your input.")
    except mysql.connector.Error as err:
        print(f"⚠️ Error : {err}")

    finally:
        cursor.close()
        conn.close()

# Update Password
def update_password(user_id, new_password):
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())


    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(query, (hashed_password, user_id))
        conn.commit()

        if cursor.rowcount > 0:
            print("✅ Password updated successfully!")
        else:
            print("❌ No changes made. Please check your input.")

    except mysql.connector.Error as err:
        print(f"⚠️ Error: {err}")

    finally:
        cursor.close()
        conn.close()

# Toggle Notifications
def toggle_notifications(user_id, enable):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "UPDATE users SET notifications_enabled = %s WHERE id =  %s"
        cursor.execute(query, (enable, user_id))
        conn.commit()

        status = "enabled" if enable else "disabled"
        print(f"🔔 Notifications {status} successfully!")

    except mysql.connector.Error as err:
        print(f" warning ⚠️Error: {err}")

    finally:
        cursor.close()
        conn.close()

# Set Financial Preferences
def set_financial_preferences(user_id, currency, savings_percentage):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "UPDATE users SET currency = %s, savings_percentage = %s WHERE id = %s"
        cursor.execute(query, (currency, savings_percentage, user_id))
        conn.commit()

        print(f"💰 Preferences updated! Currency: {currency}, Savings %: {savings_percentage}%")

    except mysql.connector.Error as err:
        print(f"⚠️ Error: {err}")

    finally:
        cursor.close()
        conn.close()

# Sample Usage
if __name__=="__main__":
    user_id = 1 # Replace with dynamic user ID
    # Uncomment to test each function
    update_username(user_id, "new_username123")
    update_password(user_id, "NewSecurePassword!")
    toggle_notifications(user_id, False)  # Disable notifications
    set_financial_preferences(user_id, "USD", 15.5)