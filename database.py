import sqlite3

def connect_db():
    return sqlite3.connect('usersdata.db')

def initialize_db():
    try:
        connection = sqlite3.connect('usersdata.db')
        cursor = connection.cursor()

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        ''')

        # Create transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        ''')

        # Create incomes table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        ''')

        # Create expenses table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        ''')

        connection.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred during database initialization: {e}")
    finally:
        connection.close()

def check_null_transaction_types():
    connection = sqlite3.connect('usersdata.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions WHERE type IS NULL;")
    null_transactions = cursor.fetchall()
    connection.close()
    return null_transactions
