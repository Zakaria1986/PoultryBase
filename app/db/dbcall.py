# docker exec -it poultrybase_app python -m app.db.dbcall  
from app.dbconfig import db_connection

def create_table():
    conn = db_connection()
   # Creates the 'chickens' table if it does not exist.
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
        conn.close()
    except Exception as e:
        print("Error creating table:", e)

if __name__ == "__main__": 
     create_table()
  
      
   
