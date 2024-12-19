from database import connect_db
from rich.console import Console
from rich.table import Table
import sqlite3

console = Console()

def connect_db():
    return sqlite3.connect('usersdata.db')

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


