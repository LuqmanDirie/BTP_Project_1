import mysql.connector
from mysql.connector import Error

def create_connection():
    """Connect to MySQL Database"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='Myapipassword',
            database='RestfulApiDatabase'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection