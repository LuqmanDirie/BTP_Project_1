import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='newdb',
            user='root',
            passwd='PHRpassword',
            database='PHRApiDatabase',
            port=3306
        )
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

def create_user(username, password, full_name, dob, gender):
    conn = create_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, password, full_name, dob, gender) 
            VALUES (%s, %s, %s, %s, %s)
        """, (username, password, full_name, dob, gender))
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except Error as e:
        print(f"Error while creating user: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_user_by_id(user_id):
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        return user
    except Error as e:
        print(f"Error fetching user by ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_users():
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users
    except Error as e:
        print(f"Error fetching all users: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_user(user_id, username, password, full_name, dob, gender):
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET username = %s, password = %s, full_name = %s, dob = %s, gender = %s
            WHERE user_id = %s
        """, (username, password, full_name, dob, gender, user_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating user: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_user(user_id):
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
