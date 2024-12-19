from database import initialize_db, check_null_transaction_types
from user import user_registration, user_login
from transaction import add_income, view_incomes, add_expense, view_expenses, view_all_transactions, delete_transaction, edit_transaction, generate_report, set_budget, check_budget
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    # Initialize the database and create tables
    initialize_db()

    # Check for transactions with NULL types
    null_transactions = check_null_transaction_types()
    if null_transactions:
        print("Transactions with NULL types found:")
        for transaction in null_transactions:
            print(transaction)
    else:
        print("No transactions with NULL types.")

    # User Registration/Login
    while True:
        print("Welcome to Personal Finance Management")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            user_registration()
        elif choice == '2':
            user_id = user_login()
            if user_id:
                print(f"Welcome User {user_id}!")
                user_menu(user_id)  # Call user_menu here after successful login
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu(user_id):
    while True:
        panel = Panel("User Menu", title="Personal Finance App", border_style="bold blue")
        console.print(panel)

        print("1. Add Income")
        print("2. View Incomes")
        print("3. Add Expense")
        print("4. View Expenses")
        print("5. View All Transactions")
        print("6. Delete Transaction")
        print("7. Edit Transaction")
        print("8. Generate Report")
        print("9. Set Budget")
        print("10. Check Budget")
        print("11. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            category = input("Enter income category: ")
            amount = float(input("Enter income amount: "))
            date = input("Enter date (YYYY-MM-DD): ")
            add_income(user_id, category, amount, date)
        elif choice == '2':
            view_incomes(user_id)
        elif choice == '3':
            category = input("Enter expense category: ")
            amount = float(input("Enter expense amount: "))
            date = input("Enter date (YYYY-MM-DD): ")
            add_expense(user_id, category, amount, date)
        elif choice == '4':
            view_expenses(user_id)
        elif choice == '5':
            view_all_transactions(user_id)
        elif choice == '6':
            transaction_id = int(input("Enter transaction ID to delete: "))
            delete_transaction(user_id, transaction_id)
        elif choice == '7':
            transaction_id = int(input("Enter transaction ID to edit: "))
            new_category = input("Enter new category: ")
            new_amount = float(input("Enter new amount: "))
            new_date = input("Enter new date (YYYY-MM-DD): ")
            edit_transaction(user_id, transaction_id, new_category, new_amount, new_date)
        elif choice == '8':
            generate_report(user_id)
        elif choice == '9':
            category = input("Enter budget category: ")
            budget_amount = float(input("Enter budget amount: "))
            set_budget(user_id, category, budget_amount)
        elif choice == '10':
            check_budget(user_id)
        elif choice == '11':
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
