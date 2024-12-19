from rich.table import Table
from rich.console import Console
import sqlite3

console = Console()

def connect_db():
    return sqlite3.connect('usersdata.db')

def generate_report(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Calculate total income and expenses
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = ?', (user_id, 'income'))
    total_income = cursor.fetchone()[0] or 0  # Default to 0 if None

    cursor.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = ?', (user_id, 'expense'))
    total_expenses = cursor.fetchone()[0] or 0  # Default to 0 if None

    conn.close()

    # Create a Rich table for the report
    report_table = Table(title="Financial Report", box=None)
    report_table.add_column("Total Income", justify="right", style="green")
    report_table.add_column("Total Expenses", justify="right", style="red")
    report_table.add_column("Balance", justify="right", style="blue")

    balance = total_income - total_expenses

    report_table.add_row(f"${total_income:.2f}", f"${total_expenses:.2f}", f"${balance:.2f}")

    # Print the report table
    console.print(report_table)

