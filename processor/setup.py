import os
import time
import mysql.connector
from mysql.connector import errorcode


DB_HOST = os.getenv('DB_HOST')  # # 'localhost'
DB_USER = os.getenv('DB_USER')  # 'iot_gb'
DB_PASSWORD = os.getenv('DB_PASSWORD')  # 'password'
DB_NAME = os.getenv('DB_NAME')  # 'iot_sensor_data'


CREATE_TABLE_QUERY = """
CREATE TABLE motion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sensor_id VARCHAR(255) NOT NULL,
    motion_detected BOOLEAN NOT NULL
);
"""

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def wait_for_db():
    deadline = time.time() + 100
    while time.time() < deadline:
        try:
            cnx = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )

            return
        except mysql.connector.Error as err:
            time.sleep(0.5)
    print("Database never came up.")
    exit(1)

def main():
    wait_for_db()

    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = cnx.cursor()
        cursor.execute(f"USE {DB_NAME}")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    # Check if the "motion" table exists
    cursor.execute("SHOW TABLES LIKE 'motion'")
    result = cursor.fetchone()

    # If the "motion" table does not exist, create it
    if not result:
        try:
            cursor.execute(CREATE_TABLE_QUERY)
            print("Table 'motion' created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err.msg}")
    else:
        print("Table 'motion' already exists.")

    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
