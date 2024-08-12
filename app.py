from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.secret_key = 'supersecretkey'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Database configuration
db_config = {
    'user': 'formuser',  # Replace with your MySQL username
    'password': 'password',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'FormPractice'
}

# Check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']

    # Save form data to the database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, phone)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'error')
        return redirect(url_for('index'))

    # Save uploaded files
    files = request.files.getlist('pdfs')
    filenames = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"user_{user_id}_{filename}")
            file.save(file_path)
            filenames.append(f"user_{user_id}_{filename}")

    # Update the database with the file names
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        for filename in filenames:
            cursor.execute("INSERT INTO user_files (user_id, filename) VALUES (%s, %s)", (user_id, filename))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'error')
        return redirect(url_for('index'))

    flash("Form submitted successfully!", 'success')
    return redirect(url_for('index'))

@app.route('/view_data')
def view_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.first_name, u.last_name, u.email, u.phone,
                   GROUP_CONCAT(f.filename SEPARATOR ',') AS filenames
            FROM users u
            LEFT JOIN user_files f ON u.id = f.user_id
            GROUP BY u.id
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'error')
        return redirect(url_for('index'))

    return render_template('view_data.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
