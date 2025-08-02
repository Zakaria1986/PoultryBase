from flask import Flask, request, render_template_string
# import mysql.connector
from dbcall import Db_connection

app = Flask(__name__)
@app.route("/")
def chickens():
    db = Db_connection()
    results = []

    # Select all data from chickens table
    chickens = db.fetch_data("SELECT * FROM chickens")
    if chickens:
        for chicken in chickens:
            results.append({'id': chicken["id"], 'name': chicken["name"]})
    else:
        print("⚠️ No data found.")

    template = """
    <h1>🐔 Chickens in Database</h1>
    {% if chickens %}
        <ul>
        {% for chicken in chickens %}
            <li>ID: {{ chicken.id }} — Name: {{ chicken.name }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>⚠️ No chickens found.</p>
    {% endif %}
    """
    return render_template_string(template, chickens=results)

  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
#     db = Db_connection()
   
#     # Ask user for a chicken name
#     chicken_name = input("Enter chicken name to add: ").strip()
#     if chicken_name:
#         success = db.add_data([chicken_name])
        
# # Select all data from chickens table
#     chickens = db.fetch_data("SELECT * FROM chickens")
#     if chickens:
#         print("Total 🐔 (Chickens) in database:", len(chickens))
#         for chicken in chickens:
#             print("chicken ID: ", chicken["id"], "- name: ", chicken["name"])
#     else:
#         print("⚠️ No data found.")

   

    
# Run the command: docker exec -it poultrybase_app python main.py  

