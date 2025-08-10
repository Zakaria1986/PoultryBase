import os
import mysql.connector

class Db_connection:
    def __init__(self, host='db', user='root', password='root', database='poultrydb'):
        # Get credentials from environment variables, with defaults for fallback/testing
        self.host = os.getenv('DB_HOST', host)
        self.user = os.getenv('DB_USER', user)
        self.password = os.getenv('DB_PASS', password)
        self.database = os.getenv('DB_NAME', database)
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("✅ Successfully connected to the database:", self.database)
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error connecting to database: {err}")
            self.connection = None # Ensure connection is None if failed
            self.cursor = None     # Ensure cursor is None if failed
            return False

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed.")

    def execute_query(self, query, params=None):
        if not self.connect(): # Connect on demand
            return False
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"❌ Query error: {err}")
            self.connection.rollback()
            return False
        finally:
            self.close_connection() # Close connection after query

    def fetch_data(self, query, params=None):
        if not self.connect(): # Connect on demand
            return None
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            print(f"❌ Query error: {err}")
            return None
        finally:
            self.close_connection() # Close connection after fetching

    def add_data(self, addNewRecord):
        if not self.connect():
            print("😢 Cannot add data without a connection.")
            return None
        try:
            sql = "INSERT INTO chickens (name) VALUES (%s)"
            self.cursor.execute(sql, addNewRecord)
            self.connection.commit()
            last_id = self.cursor.lastrowid
            print(f"✅ Record added successfully, ID: {last_id}")
            return last_id
        except mysql.connector.Error as err:
            print(f"❌ Query error: {err}")
            self.connection.rollback()
            return None
        finally:
            self.close_connection()

    def delete_data(self, chicken_id):
        if not self.connect():
            print("😢 Cannot delete data without a connection.")
            return False
        try:
            sql = "DELETE FROM chickens WHERE id = %s"
            self.cursor.execute(sql, (chicken_id,))
            self.connection.commit()
            print(f"✅ Chicken with ID {chicken_id} deleted.")
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error deleting chicken: {err}")
            self.connection.rollback()
            return False
        finally:
            self.close_connection()


    def update_data(self, chicken_id, new_name):
        if not self.connect():
            print("😢 Cannot update data without a connection.")
            return False, "Database connection failed."
        try:
            sql = "UPDATE chickens SET name = %s WHERE id = %s"
            self.cursor.execute(sql, (new_name, chicken_id))
            self.connection.commit()
            print(f"✅ Chicken with ID {chicken_id} updated.")
            return True, ""
        except mysql.connector.Error as err:
            error_msg = f"Database error: {err}"
            print(f"❌ {error_msg}")
            self.connection.rollback()
            return False, error_msg
        finally:
            self.close_connection()
