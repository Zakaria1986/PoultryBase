# import mysql.connector
from dbcall import Db_connection

if __name__ == "__main__":
    db = Db_connection()
    chickens = db.fetch_data("SELECT * FROM chickens")
    print(chickens)
    
    if chickens:
        print("🐔 Chickens in database:")
        for chicken in chickens:
            print(chicken["name"])
    else:
        print("⚠️ No data found.")
