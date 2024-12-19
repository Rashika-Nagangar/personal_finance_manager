import sqlite3
from rich.console import Console
from rich.table import Table
from database import connect_db

console = Console()

def add_income(user_id, category, amount, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, 'income', ?, ?, ?)",
        (user_id, category, amount, date)
    )
    conn.commit()
    conn.close()



def view_incomes(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT category, amount, date FROM transactions WHERE user_id = ? AND type = 'income'", (user_id,))
    incomes = cursor.fetchall()
    conn.close()

    if not incomes:
        print("No incomes found.")
    else:
        # Create a Rich table to display incomes
        table = Table(title="Income Records", box=None)
        table.add_column("Category", justify="left", style="cyan")
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Date", justify="right", style="magenta")

        for category, amount, date in incomes:
            table.add_row(category, f"${amount:.2f}", date)

        console.print(table)


def add_expense(user_id, category, amount, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, 'expense', ?, ?, ?)",
        (user_id, category, amount, date)
    )
    conn.commit()
    conn.close()
    print("Expense added successfully.")

def view_expenses(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT category, amount, date FROM transactions WHERE user_id = ? AND type = 'expense'", (user_id,))
    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("No expenses found.")
    else:
        # Create a Rich table to display expenses
        table = Table(title="Expense Records", box=None)
        table.add_column("Category", justify="left", style="cyan")
        table.add_column("Amount", justify="right", style="red")
        table.add_column("Date", justify="right", style="magenta")

        for category, amount, date in expenses:
            table.add_row(category, f"${amount:.2f}", date)

        console.print(table)

def view_all_transactions(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, category, amount, date FROM transactions WHERE user_id = ?', (user_id,))
    transactions = cursor.fetchall()

    # Create a Rich table for transactions
    transaction_table = Table(title="All Transactions", box=None)
    transaction_table.add_column("ID", justify="right", style="cyan")
    transaction_table.add_column("Type", justify="left", style="magenta")
    transaction_table.add_column("Category", justify="left", style="green")
    transaction_table.add_column("Amount", justify="right", style="red")
    transaction_table.add_column("Date", justify="center", style="blue")

    if transactions:
        for transaction in transactions:
            transaction_table.add_row(str(transaction[0]), transaction[1], transaction[2], f"${transaction[3]:.2f}", transaction[4])
    else:
        transaction_table.add_row("No transactions found.", "", "", "", "")  # Handle no transactions case

    # Print the transaction table
    console.print(transaction_table)

    conn.close()


def delete_transaction(user_id, transaction_id):
    connection = sqlite3.connect('usersdata.db')
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
        connection.commit()
        print("Transaction deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting transaction: {e}")
    finally:
        connection.close()

def edit_transaction(user_id, transaction_id, new_category, new_amount, new_date):
    connection = sqlite3.connect('usersdata.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
            UPDATE transactions 
            SET category = ?, amount = ?, date = ? 
            WHERE id = ? AND user_id = ?
        """, (new_category, new_amount, new_date, transaction_id, user_id))
        connection.commit()
        print("Transaction updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while updating transaction: {e}")
    finally:
        connection.close()

def generate_report(user_id):
    conn = connect_db()  # Ensure you have a function to connect to your database
    cursor = conn.cursor()
    
    # Fetch all transactions for the user
    cursor.execute('SELECT type, category, amount, date FROM transactions WHERE user_id = ?', (user_id,))
    transactions = cursor.fetchall()

    # Calculate totals
    total_income = sum(amount for (type, category, amount, date) in transactions if type == 'income')
    total_expense = sum(amount for (type, category, amount, date) in transactions if type == 'expense')
    balance = total_income - total_expense

    # Create a Rich table for the report
    table = Table(title="Financial Report", box=None)
    table.add_column("Category", justify="left", style="cyan")
    table.add_column("Total Income", justify="right", style="green")
    table.add_column("Total Expense", justify="right", style="red")
    table.add_column("Balance", justify="right", style="magenta")

    # Adding rows for income and expense categories
    income_row = ["Income", f"${total_income:.2f}", "-", f"${balance:.2f}"]
    expense_row = ["Expense", "-", f"${total_expense:.2f}", f"${balance:.2f}"]

    table.add_row(*income_row)
    table.add_row(*expense_row)

    # Display the report
    console.print(table)

    conn.close()

def set_budget(user_id, category, budget_amount):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if a budget already exists for this category
    cursor.execute("SELECT * FROM budgets WHERE user_id = ? AND category = ?", (user_id, category))
    existing_budget = cursor.fetchone()

    if existing_budget:
        # Update the existing budget
        cursor.execute("UPDATE budgets SET budget_amount = ? WHERE user_id = ? AND category = ?", 
                       (budget_amount, user_id, category))
        print(f"Budget for category '{category}' updated to ${budget_amount:.2f}.")
    else:
        # Insert a new budget
        cursor.execute("INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)", 
                       (user_id, category, budget_amount))
        print(f"Budget for category '{category}' set to ${budget_amount:.2f}.")
    
    conn.commit()
    conn.close()

def check_budget(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT category, budget_amount FROM budgets WHERE user_id = ?", (user_id,))
    budgets = cursor.fetchall()
    conn.close()

    if not budgets:
        print("No budgets set.")
    else:
        # Create a Rich table to display budgets
        table = Table(title="Budget Overview", box=None)
        table.add_column("Category", justify="left", style="cyan")
        table.add_column("Budget Amount", justify="right", style="magenta")

        for category, budget_amount in budgets:
            table.add_row(category, f"${budget_amount:.2f}")

        console.print(table)

def initialize_database():
    conn = sqlite3.connect('usersdata.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        type TEXT,
                        category TEXT,
                        amount REAL,
                        date TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')
    conn.commit()
    conn.close()

# Call this function when your app starts
initialize_database()
