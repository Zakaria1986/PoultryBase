# import mysql.connector
from dbcall import Db_connection

if __name__ == "__main__":
    db = Db_connection()
    
    addNewRecord = []
   
    # Ask user for a chicken name
    chicken_name = input("Enter chicken name to add: ").strip()
    if chicken_name:
        success = db.add_data([chicken_name])
        

    chickens = db.fetch_data("SELECT * FROM chickens")
    if chickens:
        print("Total 🐔 (Chickens) in database:", len(chickens))
        for chicken in chickens:
            print("chicken ID: ", chicken["id"], "- name: ", chicken["name"])
    else:
        print("⚠️ No data found.")

   

       



      # Run the command: docker exec -it poultrybase_app python main.py  

