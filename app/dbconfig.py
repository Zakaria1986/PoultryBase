import os
import mysql.connector

# def db_connection():
#     try:
#         conn = mysql.connector.connect(
#             host=os.getenv('DB_HOST', 'db'),
#             user=os.getenv('DB_USER', 'root'),
#             password=os.getenv('DB_PASS', 'root'),
#             database=os.getenv('DB_NAME', 'poultrydb')
#         )
#         print("Successfully connected to the database:", conn.database)

#     except mysql.connector.Error as err:
#         print("Error connecting to database:", err)

# if __name__ == "__main__":
#    conn = db_connection() # runs only if you do: python dbconfig.py
#    conn()
#    conn.close()
    
def db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'db'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASS', 'root'),
            database=os.getenv('DB_NAME', 'poultrydb')
        )
        print("Successfully connected to the database:", conn.database)
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return None

def create_table(conn):
    if conn is None:
        print("Failed to connect to database, cannot create table.")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chickens (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
            """)
        conn.commit()
        print("Table 'chickens' ensured.")
    except Exception as e:
        print("Error creating table:", e)

def insert_chicken(conn, name):
    if conn is None:
        print("No database connection, cannot insert data.")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO chickens (name) VALUES (%s)", (name,))
        conn.commit()
        print(f"Inserted chicken: {name}")
    except Exception as e:
        print("Error inserting data:", e)

def init_data(conn):
    # List of initial chicken names
    chickens = ['George', 'Fleur', 'Devon', 'Casey', 'Marigold', 'Apple Mint']
    for name in chickens:
        insert_chicken(conn, name)

if __name__ == "__main__":
    conn = db_connection()
    if conn:
        create_table(conn)
        init_data(conn)
        conn.close()
    else:
        print("Failed to connect to database.")