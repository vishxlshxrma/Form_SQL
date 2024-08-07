from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'formuser',  # or 'root' if you use the root user
    'password': 'password',  # replace with your MySQL password
    'host': 'localhost',
    'database': 'FormPractice'
}

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, email, phone))
        conn.commit()
        cursor.close()
        conn.close()
        return 'Form submitted successfully!'
    except mysql.connector.Error as err:
        return f'Error: {err}'

if __name__ == '__main__':
    app.run(debug=True)
