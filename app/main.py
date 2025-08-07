from flask import Flask, request, render_template, render_template_string, redirect, url_for, flash

from dbcall import Db_connection




app = Flask(__name__)

def initialize_database():
    """Create the chickens table if it doesn't exist"""
    db = Db_connection()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS chickens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """
    try:
        db.execute_query(create_table_sql)
    except Exception as e:
        flash(f"Database initialization error: {str(e)}", "error")
    finally:
        db.close()

@app.route("/", methods=["GET", "POST"])
def chickens():
    db = Db_connection()
    results = []

    # Handle DELETE via POST (HTML forms don’t support DELETE directly)
    if request.method == "POST":
        chicken_id = request.form.get("id")
        if chicken_id:
            db.delete_data(chicken_id)


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


@app.route("/add", methods=["GET", "POST"])
def add_chicken():
    if request.method == "POST":
        db = Db_connection()
        chicken_name = request.form.get("name")
        if chicken_name:
            try:
                new_id = db.add_data((chicken_name,))
                db.close()
                flash(f"✅ Successfully added chicken with ID {new_id}", "success")
                return redirect(url_for('chickens'))
            except Exception as e:
                db.close()
                flash(f"Database error: {str(e)}", "error")
                # Continue to show the form with error message
    
    # GET request or failed POST - show the form
    add_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add New Chicken</title>
    </head>
    <body>
        <h1>🐔 Add New Chicken</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flashes">
                {% for category, message in messages %}
                    <p class="{{ category }}">{{ message }}</p>
                {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        <form method="POST">
            <label for="name">Chicken Name:</label>
            <input type="text" id="name" name="name" required>
            <button type="submit">Add Chicken</button>
        </form>
        <a href="{{ url_for('chickens') }}">Back to List</a>
    </body>
    </html>
    """
    return render_template_string(add_form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    
# Run the command: docker exec -it poultrybase_app python main.py  

