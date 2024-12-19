import pytest
import sqlite3
import bcrypt  # Make sure bcrypt is imported
from features.user_auth import register_user, login_user, fetch_query

# Assuming you have a fetch_query function defined somewhere
def fetch_query(query, params):
    # Here, replace 'your_test_database.db' with your test database name
    with sqlite3.connect('your_test_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

@pytest.fixture(scope='module', autouse=True)
def setup_test_db():
    # Create a test database and users table before tests run
    conn = sqlite3.connect('your_test_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    yield
    # Clean up the database after tests
    cursor.execute('DROP TABLE IF EXISTS users')
    conn.commit()
    conn.close()

# tests/test_user_auth.py

def test_register_user(setup_test_db):
    username = "test_user"
    password = "test_pass"

    # Register the user
    register_user(username, password)

    # Check if the user exists in the database
    user = fetch_query("SELECT * FROM users WHERE username = ?", (username,))
    print("Fetched user:", user)  # Debugging line to see if the user was inserted
    assert user is not None
    assert bcrypt.checkpw(password.encode(), user[0][2].encode())


def test_login_user(monkeypatch, setup_test_db):
    # Mocking input for the test
    def mock_input(prompt):
        return "test_user" if "username" in prompt else "test_pass"

    monkeypatch.setattr('builtins.input', mock_input)
    
    # Test login
    assert login_user() is True
