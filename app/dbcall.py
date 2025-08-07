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
        
    def add_data(self, addNewRecord):
        conn = self.connect()
        if not conn:
            print("😢 Cannot fetch data without a connection.")
            return None
        try:
            cursor = conn.cursor(dictionary=True)

            sql = "INSERT INTO chickens (name) VALUES (%s)"
            # val = ("John", "Highway 21")
            cursor.execute(sql, addNewRecord)
            conn.commit()
            print("✅ Record added successfully:", cursor.rowcount)
            last_id = cursor.lastrowid
            print("Last inserted ID:", last_id)  # Debugging line to check the last inserted ID
            # Return the last inserted ID
            # Fetch the last inserted ID
            cursor.close()
            conn.close()
            # return print(last_id)         
        except mysql.connector.Error as err:
            print("❌ Query error:", err)
            return None
        
    def delete_data(self, chicken_id):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM chickens WHERE id = %s"
            cursor.execute(sql, (chicken_id,))
            conn.commit()
            print(f"✅ Chicken with ID {chicken_id} deleted.")
            return True
        except mysql.connector.Error as err:
            print("❌ Error deleting chicken:", err)
            return False
        finally:
            cursor.close()
            conn.close()


    def update_data(self, chicken_id, new_name):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            sql = "UPDATE chickens SET name = %s WHERE id = %s"
            cursor.execute(sql, (new_name, chicken_id))
            conn.commit()
        except mysql.connector.Error as err:
            error_msg = f"Database error: {err}"
            print(f"❌ {error_msg}")
            conn.rollback()
            return False, error_msg
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()