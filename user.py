import sqlite3

def user_registration():
    username = input("Enter username: ")
    password = input("Enter password: ")

    connection = sqlite3.connect('usersdata.db')
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")
    except sqlite3.Error as e:
        print(f"An error occurred during registration: {e}")
    finally:
        connection.close()

def user_login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    connection = sqlite3.connect('usersdata.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    connection.close()

    if user:
        print("Login successful.")
        return user[0]  # Return user ID
    else:
        print("Invalid username or password.")
        return None
