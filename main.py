from auth import signup, login
from bill_reminders import add_recurring_bill, view_recurring_bills, check_and_process_bills
from budget import set_budget, view_budget
from dashboard import show_dashboard
from export_import import export_transactions_to_csv, import_transactions_from_csv
from goals import add_goal, view_goals, update_goal_progress, delete_goal
from insights import categorize_expense, show_spending_insights
from investments import add_investment, view_investments, delete_investment
from notifications import check_due_bills, check_low_balance, check_goal_deadlines
from reports import monthly_expenses_summary, category_expense_summary, income_vs_expense
from security import backup_database, restore_database, encrypt_data, decrypt_data
from settings import update_password, update_username, toggle_notifications, set_financial_preferences
from transactions import add_transaction, view_transactions, delete_transaction

#Display the Menu
def display_menu():
    print("\n=== Personal Finance Manager ===")
    print("1. Dashboard")
    print("2. Add Transaction")
    print("3. View Transactions")
    print("4. Delete Transaction")
    print("5. Set Budget")
    print("6. View Budget")
    print("7. Add Recurring Bill")
    print("8. View Recurring Bills")
    print("9. Process Due Bills")
    print("10. Add Goal")
    print("11. View Goals")
    print("12. Update Goal Progress")
    print("13. Delete Goal")
    print("14. Categorize Expense")
    print("15. Show Spending Insights")
    print("16. Add Investment")
    print("17. View Investments")
    print("18. Delete Investment")
    print("19. Check Notifications")
    print("20. Export Transactions")
    print("21. Import Transactions")
    print("22. Backup Database")
    print("23. Restore Database")
    print("24. Encrypt Data")
    print("25. Decrypt Data")
    print("26. Update Settings")
    print("27. Monthly Expenses Summary")
    print("28. Category-wise Expense Summary")
    print("29. Income vs Expense Comparison")
    print("30. Exit")

# Main program
def main():
    print("Welcome to Personal Finance Manager!")

    # Authentication loop
    user_id = None
    while not user_id:
        print("\n1. Login\n2. Signup")
        auth_choice = input("Choice: ")

        if auth_choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            user_id = login(username, password)
            if user_id:
                print(f"Logged in with user ID: {user_id}")
        elif auth_choice == "2":
            username = input("New Username: ")
            password = input("Set Password: ")
            user_id = signup(username, password)
            if user_id:
                print(f"Signed Up With User ID: {user_id}")
        else:
            print("❌ Invalid Choice! Try Again.")

    #Main menu loop
    while True:
        display_menu()
        choice = input("Enter Your Choice: ")

        try:
            if choice == "1":
                show_dashboard(user_id)
            elif choice == "2":
                amount = float(input("Amount: "))
                category = input("Category: ")
                type_ = input("Type (Income/Expense): ")
                add_transaction(user_id, amount, category, type_)
            elif choice == "3":
                view_transactions(user_id)
            elif choice == "4":
                trans_id = int(input("Transaction ID to Delete: "))
                delete_transaction(trans_id)
            elif choice == "5":
                category = input("Category: ")
                amount = float(input("Budget Amount: "))
                set_budget(category, amount)
            elif choice == "6":
                view_budget()
            elif choice == "7":
                category = input("Category: ")
                amount = float(input("Amount: "))
                due_date = input(" Due Date (YYYY-MM-DD): ")
                frequency = input("Frequency (Weekly/Monthly): ")
                add_recurring_bill(user_id,category, amount, due_date, frequency)
            elif choice == "8":
                view_recurring_bills(user_id)
            elif choice == "9":
                check_and_process_bills(user_id)
            elif choice == "10":
                goal_name = input("Goal Name: ")
                target_amount = float(input("Target Amount: "))
                deadline = input("Deadline (YYYY-MM-DD): ")
                add_goal(user_id, goal_name, target_amount, deadline)
            elif choice == "11":
                view_goals(user_id)
            elif choice == "12":
                goal_id = int(input("Goal ID: "))
                amount = float(input("Amount to Add: "))
                update_goal_progress(goal_id, amount)
            elif choice == "13":
                goal_id = int(input("Goal ID to delete: "))
                delete_goal(goal_id)
            elif choice == "14":
                trans_id = int(input("Transaction ID: "))
                cat_id = int(input("Category ID: "))
                categorize_expense(trans_id, cat_id)
            elif choice == "15":
                show_spending_insights(user_id)
            elif choice == "16":
                inv_name = input("Investment Name: ")
                amount = float(input("Amount: "))
                inv_type = input("Type (e.g., Stock,..)")
                purchase_date = input("Purchase Date (YYYY-MM_DD): ")
                return_rate = float(input("Return Rate (%): "))
                add_investment(user_id, inv_name, amount, inv_type, purchase_date, return_rate)
            elif choice == "17":
                view_investments(user_id)
            elif choice == "18":
                inv_id = int(input("Investment ID to Delete"))
                delete_investment(inv_id)
            elif choice == "19":
                check_due_bills(user_id)
                threshold = float(input("Low Balance Threshold: "))
                check_low_balance(user_id, threshold)
                check_goal_deadlines(user_id)
            elif choice == "20":
                filename = input("Export Filename (e.g., transactions.csv): ")
                export_transactions_to_csv(user_id, filename)
            elif choice == "21":
                filename = input("Import Filename: ")
                import_transactions_from_csv(user_id, filename)
            elif choice == "22":
                backup_database()
            elif choice == "23":
                backup_file = input("Backup File Path")
                restore_database(backup_file)
            elif choice == "24":
                text = input("Text to encrypt: ")
                encrypted = encrypt_data(text)
                print(f"Encrypted: {encrypted}")
            elif choice == "25":
                text = input("Text to Decrypt: ")
                decrypted = decrypt_data(text)
                print(f"Decrypted: {decrypted}")
            elif choice == "26":
                print("1. Update Username\n2. Update Password\n3. Toggle Notifications\n4. Set Preferences")
                sub_choice = input("Settings Choice: ")
                if sub_choice == "1":
                    new_username = input("New Username: ")
                    update_username(user_id, new_username)
                elif sub_choice == "2":
                    new_password  = input("New Password: ")
                    update_password(user_id, new_password)
                elif sub_choice == "3":
                    enable = input("Enable notifications? (yes/no): ").lower() == "yes"
                    toggle_notifications(user_id, enable)
                elif sub_choice == "4":
                    currency = input("Currency (e.g., INR): ")
                    savings_pct = float(input("Savings Percentage: "))
                    set_financial_preferences(user_id, currency, savings_pct)
            elif choice == "27":
                monthly_expenses_summary(user_id)
            elif choice == "28":
                category_expense_summary(user_id)
            elif choice == "29":
                income_vs_expense(user_id)
            elif choice == "30":
                print("Goodbye!")
                break
            else:
                print("❌ Invalid Choice! please Try Again.")
        except ValueError as e:
            print(f"❌ Invalid Input: {e}. Please enter valid data.")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

