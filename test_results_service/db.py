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

def create_test_result(user_id, test_type, result_date, result, notes):
    """ Insert a new test result into the test_results table. """
    conn = create_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO test_results (user_id, test_type, result_date, result, notes) 
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, test_type, result_date, result, notes))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error creating test result: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_test_result_by_id(result_id):
    """ Fetch a single test result by result_id. """
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM test_results WHERE result_id = %s", (result_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching test result by ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_test_results_for_user(user_id):
    """ Fetch all test results for a specific user. """
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM test_results WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching test results for user: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_test_result(result_id, user_id, test_type, result_date, result, notes):
    """ Update a test result in the test_results table. """
    conn = create_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE test_results SET
            user_id = %s,
            test_type = %s,
            result_date = %s,
            result = %s,
            notes = %s
            WHERE result_id = %s
        """, (user_id, test_type, result_date, result, notes, result_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating test result: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_test_result(result_id):
    """ Delete a test result from the test_results table. """
    conn = create_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM test_results WHERE result_id = %s", (result_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting test result: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
