from flask import Flask, request, render_template, render_template_string, redirect, url_for, flash
from dbcall import Db_connection  # Corrected import for internal module

import os

app = Flask(__name__)

def initialize_database():
    """Create the chickens table if it doesn't exist (MySQL compatible)"""
    db = Db_connection()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS chickens (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB;
    """
    try:
        db.execute_query(create_table_sql)
    except Exception as e:
        flash(f"Database initialization error: {str(e)}", "error")
    finally:
        db.close_connection() # Use close_connection method

@app.route("/", methods=["GET", "POST"])
def chickens():
    db = Db_connection()
    results = []

    initialize_database()

    # Handle DELETE via POST (HTML forms don’t support DELETE directly)
    if request.method == "POST":
        chicken_id = request.form.get("id")
        if chicken_id:
            db.delete_data(chicken_id)

    chickens = db.fetch_data("SELECT * FROM chickens")
    db.close_connection() # Ensure connection is closed after use
    if chickens:
        results = chickens
    return render_template("index.html", chickens=chickens)

@app.route("/add", methods=["GET", "POST"])
def add_chicken():
    if request.method == "POST":
        db = Db_connection()
        chicken_name = request.form.get("name")
        if chicken_name:
            new_id = db.add_data((chicken_name,))
            db.close_connection() # Ensure connection is closed after use
            return redirect(url_for('chickens')) # Redirect after successful add
    return render_template("add.html")



@app.route("/edit/<int:chicken_id>", methods=["GET", "POST"])
def editForm(chicken_id):
    db = Db_connection()
    chicken = db.fetch_data(f"SELECT * FROM chickens WHERE id = {chicken_id}")
    db.close_connection() # Ensure connection is closed after use
    
    if chicken:
        chicken = chicken[0] # fetch_data returns a list, get the first item

    if request.method == "POST":
        db_post = Db_connection() # Create a new connection for the POST request
        new_name = request.form.get("name").strip()
        success, error_msg = db_post.update_data(chicken_id, new_name)
        db_post.close_connection() # Ensure connection is closed after use
        if success:
            flash("Update successful", "success")
            return redirect(url_for('chickens'))
        else:
            flash(error_msg, "error")
            return redirect(url_for('editForm', chicken_id=chicken_id)) 
            # Stay on the edit page with error
        
    return render_template("update.html", chicken=chicken)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
