
import hashlib
from db_config import get_connection

# Need to insert Email function! Captcha to be done in the refining sequances, and need to automate table creation in psql instead of doing by hand

# Hash password function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# get_connection()

# Check if a user exists
def user_exists(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM UserTbl WHERE username = %s", (username,))
    result = cur.fetchone()
    conn.close()
    if result:
      return result
      
def validate_password_strength(password):
  if len(password) <= 12 or len(password) >=6:
    print("Hello")

  
# Register a new user
def register():
    print("=== Register ===")
    username = input("Enter a username: ")
    if user_exists(username):
        print("Username already exists. Please choose another.")
        return
    password = input("Enter a password: ")
    hashed_password = hash_password(password)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO UserTbl (username, password_hash) VALUES (%s, %s)", 
                    (username, hashed_password))
        conn.commit()
        print("Registration successful!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Validate user credentials
def validate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM UserTbl WHERE username = %s", (username,))
    result = cur.fetchone()
    conn.close()
    if result is None:
        return False
    return hash_password(password) == result[0]

# Login user
def login():
    print("=== Login ===")
    username = input("Enter your username: ")##
    if not user_exists(username):
        print("Username does not exist.")##
        return
    password = input("Enter your password: ")##
    if validate_user(username, password):
        print("Login successful!")
        return True
    else:
        print("Incorrect password.")##
        return False

# Reset user password
def reset_password():
    print("=== Reset Password ===")
    username = input("Enter your username: ") ##
    if not user_exists(username):
        print("Username does not exist.") ##
        return
    new_password = input("Enter a new password: ") ##
    hashed_password = hash_password(new_password)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE UserTbl SET password_hash = %s WHERE username = %s", 
                    (hashed_password, username))
        conn.commit()
        print("Resetted") ##
    except Exception as e:
        print(f"Error: {e}") ##
    finally:
        conn.close()

