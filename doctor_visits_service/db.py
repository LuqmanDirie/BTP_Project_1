import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection to the MySQL server."""
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
        print(f"Error connecting to MySQL Database: {e}")
        return None

def create_doctor_visit(user_id, visit_date, doctor_name, purpose, notes):
    """Insert a new doctor visit into the doctor_visits table."""
    conn = create_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO doctor_visits (user_id, visit_date, doctor_name, purpose, notes) 
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, visit_date, doctor_name, purpose, notes))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error creating doctor visit record: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_doctor_visit_by_id(visit_id):
    """Fetch a single doctor visit by visit_id."""
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctor_visits WHERE visit_id = %s", (visit_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching doctor visit by ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_doctor_visits_for_user(user_id):
    """Fetch all doctor visits for a specific user."""
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctor_visits WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching doctor visits for user: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_doctor_visit(visit_id, user_id, visit_date, doctor_name, purpose, notes):
    """Update a doctor visit in the doctor_visits table."""
    conn = create_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE doctor_visits SET
            user_id = %s,
            visit_date = %s,
            doctor_name = %s,
            purpose = %s,
            notes = %s
            WHERE visit_id = %s
        """, (user_id, visit_date, doctor_name, purpose, notes, visit_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating doctor visit record: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_doctor_visit(visit_id):
    """Delete a doctor visit from the doctor_visits table."""
    conn = create_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctor_visits WHERE visit_id = %s", (visit_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting doctor visit record: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
