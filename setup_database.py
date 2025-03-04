import mysql.connector

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS finance_db")
    print("Database 'finance_db' created successfully")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conn.close()

# Reconnect to MySQL, now selecting the 'finance_db' database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finance_db"
    )
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            notifications_enabled BOOLEAN DEFAULT TRUE,
            currency VARCHAR(3) DEFAULT 'INR',
            savings_percentage DECIMAL(5,2) DEFAULT 0.00
        )
    """)

    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            category VARCHAR(50) NOT NULL,
            type ENUM('income', 'expense') NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Create recurring_bills table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recurring_bills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            category VARCHAR(255) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            due_date DATE NOT NULL,
            frequency ENUM('weekly', 'monthly') NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Create budgets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            category VARCHAR(50) PRIMARY KEY,
            amount DECIMAL(10,2) NOT NULL
        )
    """)

    # Create goals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            goal_name VARCHAR(255) NOT NULL,
            target_amount DECIMAL(10,2) NOT NULL,
            saved_amount DECIMAL(10,2) DEFAULT 0.00,
            deadline DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Create investments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            investment_name VARCHAR(255) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            investment_type VARCHAR(50) NOT NULL,
            purchase_date DATE NOT NULL,
            return_rate DECIMAL(5,2) DEFAULT 0.00,
            current_value DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Create expense_categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expense_categories (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(50) UNIQUE NOT NULL
        )
    """)

    # Create categorized_expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorized_expenses (
            transaction_id INT NOT NULL,
            category_id INT NOT NULL,
            PRIMARY KEY (transaction_id, category_id),
            FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES expense_categories(category_id) ON DELETE CASCADE
        )
    """)

    # Create accounts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            balance DECIMAL(10,2) DEFAULT 0.00,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Create backups table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS backups (
            id INT AUTO_INCREMENT PRIMARY KEY,
            backup_file VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    print("All tables created successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conn.close()