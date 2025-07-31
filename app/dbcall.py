import os
import mysql.connector

class Db_connection:
    def __init__(self, host='db', user='root', password='root', database='poultrydb'):
        self.host = os.getenv('DB_HOST', host)
        self.user = os.getenv('DB_USER', user)
        self.password = os.getenv('DB_PASS', password)
        self.database = os.getenv('DB_NAME', database)

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if conn.is_connected():
                print("✅ Successfully connected to the database:", conn.database)
                return conn
            else:
                print("⚠️ Connection failed after attempt.")
                return None
        except mysql.connector.Error as err:
            print("❌ Error connecting to database:", err)
            return None

    def fetch_data(self, query):
        conn = self.connect()
        if not conn:
            print("😢 Cannot fetch data without a connection.")
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except mysql.connector.Error as err:
            print("❌ Query error:", err)
            return None
