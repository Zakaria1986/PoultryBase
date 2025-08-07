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
     <nav><a href="{{ url_for('add_chicken') }}" class="button">➕ Add New Chicken</a></nav>
    {% if chickens %}
        <ul>   
        {% for chicken in chickens %}
            <li>
                ID: {{ chicken.id }} — Name: {{ chicken.name }}
                <a href="{{ url_for('editForm', chicken_id=chicken.id) }}" class="button">✏️ Edit</a>
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
    return render_template_string(template, chickens=chickens)


@app.route("/add", methods=["GET", "POST"])
def add_chicken():
    if request.method == "POST":
        db = Db_connection()
        chicken_name = request.form.get("name")
        if chicken_name:
            new_id = db.add_data((chicken_name,))

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
        <a href="{{ url_for('chickens') }}">Home</a>
    </body>
    </html>
    """
    return render_template_string(add_form)


@app.route("/edit/<int:chicken_id>", methods=["GET", "POST"])
def editForm(chicken_id):
    db = Db_connection()
    result = db.fetch_data(f"SELECT * FROM chickens WHERE id = {chicken_id}")
    chicken_id = chicken_id
    if request.method == "POST":
        # Get only the name from form data
        new_name = request.form.get("name").strip()
        # Update using the URL parameter
        success = db.update_data(chicken_id, new_name)
        
    template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{% if chicken %}Update Chicken #{{ chicken.id }}{% else %}Error{% endif %}</title>
            <style>
                .alert { padding: 10px; margin: 10px 0; }
                .alert-error { background: #f2dede; color: #a94442; }
                form { margin: 20px; padding: 20px; border: 1px solid #ddd; }
            </style>
        </head>
        <body>
            {% if chicken %}
                <h1>Update Chicken #{{ chicken.id }}</h1>
                <form method="POST">
                    <div>
                        <label>Name: 
                            <input type="text" name="name" value="{{ chicken.name }}" required>
                        </label>
                    </div>
                    <button type="submit">Update</button>
                    <a href="{{ url_for('chickens') }}">Cancel</a>
                </form>
            {% else %}
                <div class="alert alert-error">
                    Chicken not found! <a href="{{ url_for('chickens') }}">Back to list</a>
                </div>
            {% endif %}
            
            {# Flash messages #}
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </body>
        </html>
        """    
    return render_template_string(template_str, chicken=result)



# @app.route("/update/<int:chicken_id>", methods=["GET", "POST"])
# def update_chicken(chicken_id):  # ID comes from URL only
#     db = Db_connection()
    
#     if request.method == "POST":
#         # Get only the name from form data
#         new_name = request.form.get("name").strip()
        
#         # Update using the URL parameter
#         success = db.update_data(chicken_id, new_name)
#         if success:
#             flash("Update successful", "success")
    
#     # GET request - show form
#     chicken = db.fetch_data("SELECT * FROM chickens WHERE id = {chicken_id}")
#     if not chicken:
#         flash("Chicken not found", "error")
#         return redirect(url_for('chickens'))
    
#     return render_template_string("""
#         <form method="POST">
#             <h2>Update Chicken #{{ chicken.id }}</h2>
#             <label>Name: 
#                 <input type="text" name="name" value="{{ chicken.name }}" required>
#             </label>
#             <button type="submit">Update</button>
#             <a href="{{ url_for('chickens') }}">Cancel</a>
#         </form>
        
#     """, chicken=chicken)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    
# Run the command: docker exec -it poultrybase_app python main.py  

