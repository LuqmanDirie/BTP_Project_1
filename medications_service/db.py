import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Create a database connection to the MySQL server. """
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

def create_medication(user_id, medication_name, dosage, start_date, end_date, reason):
    """ Insert a new medication into the medications table. """
    conn = create_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO medications (user_id, medication_name, dosage, start_date, end_date, reason) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, medication_name, dosage, start_date, end_date, reason))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error creating medication record: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_medication_by_id(medication_id):
    """ Fetch a single medication by medication_id. """
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM medications WHERE medication_id = %s", (medication_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching medication by ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_medications_for_user(user_id):
    """ Fetch all medications for a specific user. """
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM medications WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching medications for user: {e}")
        return None
    finally:
        cursor.close()
        conn.close()



def update_medication(medication_id, user_id, medication_name, dosage, start_date, end_date, reason):
    """ Update a medication in the medications table. """
    conn = create_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE medications SET
            user_id = %s,
            medication_name = %s,
            dosage = %s,
            start_date = %s,
            end_date = %s,
            reason = %s
            WHERE medication_id = %s
        """, (user_id, medication_name, dosage, start_date, end_date, reason, medication_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating medication record: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_medication(medication_id):
    """ Delete a medication from the medications table. """
    conn = create_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medications WHERE medication_id = %s", (medication_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting medication record: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
