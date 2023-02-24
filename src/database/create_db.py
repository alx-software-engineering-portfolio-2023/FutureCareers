"""
If your using any other database other than sqlite3
This script will create your databasep.
"""

import mysql.connector


def create_database(DB_NAME):
    """Will create the database if it doesn't exist in MySQL Server"""

    my_db = mysql.connector.connect(host="localhost",
                                    user="root",
                                    passwd="Legend1240s26#"
                                    )

    my_cursor = my_db.cursor()

    my_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

    my_cursor.close()
    my_db.close()
