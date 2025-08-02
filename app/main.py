from flask import Flask, request, render_template_string, redirect, url_for
from dbcall import Db_connection

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chickens():
    db = Db_connection()
    results = []

    # Handle DELETE via POST (HTML forms don’t support DELETE directly)
    if request.method == "POST":
        chicken_id = request.form.get("id")
        if chicken_id:
            db.delete_data(chicken_id)
            # conn = db.connect()
            # if conn:
            #     try:
                #     cursor = conn.cursor()
                #     cursor.execute("DELETE FROM chickens WHERE id = %s", (chicken_id,))
                #     conn.commit()
                #     cursor.close()
                #     db.close(conn)
                #     print(f"✅ Deleted chicken with ID {chicken_id}")
                # except Exception as e:
                #     print("❌ Error deleting record:", e)

    # Fetch chickens after possible delete
    chickens = db.fetch_data("SELECT * FROM chickens")
    if chickens:
        results = chickens

    template = """
    <h1>🐔 Chickens in Database</h1>
    {% if chickens %}
        <ul>
        {% for chicken in chickens %}
            <li>
                ID: {{ chicken.id }} — Name: {{ chicken.name }}
                <form method="POST" style="display:inline;">
                    <input type="hidden" name="id" value="{{ chicken.id }}">
                    <button type="submit">Delete</button>
                </form>
            </li>
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

