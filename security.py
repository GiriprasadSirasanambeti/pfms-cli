import os
import mysql.connector
from datetime import datetime
from cryptography.fernet import Fernet

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )

# Load or Generate Encryption Key
def load_or_generate_key():
    key_file = "encryption.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            return file.read()
    else:
        key =  Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
        return key
SECRET_KEY = load_or_generate_key()
cipher = Fernet(SECRET_KEY)

#Encrypt data
def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

#decrypt Data
def decrypt_data(data):
    return cipher.decrypt(data.encode()).decode()

# Backup Database
def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backups/backup_{timestamp}.sql"
    os.makedirs("backups", exist_ok=True)

    command = f"mysqldump -u root --password='' finance_db > {backup_file}"
    if os.system(command) == 0:
        print(f"✅ Backup created: {backup_file}")
        save_backup_record(backup_file)
    else:
        print("❌ Backup failed.")

# Save Backup Record to Database
def save_backup_record(backup_file):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO backups (backup_file) VALUES (%s)", (backup_file))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Restore Database
def restore_database(backup_file):
    if not os.path.exists(backup_file):
        print("❌ Backup file not found!")
        return
    command = f"mysql -u root --password='' finance_db < {backup_file}"
    if os.system(command) == 0:
        print(f"✅ Database restored from: {backup_file}")
    else:
        print("❌ Restore failed.")

#sample usage
if __name__ =="__main__":
    print("\n🔐 SECURITY & BACKUP MENU")
    print("1️⃣ Encrypt Data")
    print("2️⃣ Decrypt Data")
    print("3️⃣ Backup Database")
    print("4️⃣ Restore Database")

    choice = input("\nEnter Your Choice: ")

    if choice == "1":
        text = input("Enter text to encrypt: ")
        print("🔐 Encrypted:", encrypt_data(text))
    elif choice =="2":
        text = input("Enter text to decrypt: ")
        print("lock🔓 Decrypted:",decrypt_data(text))
    elif choice == "3":
        backup_database()
    elif choice == "4":
        file = input("Enter Backup file Path:")
        restore_database(file)
    else:
        print("❌ Invalid choice!")

