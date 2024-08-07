import mysql.connector

# Database configuration
db_config = {
    'user': 'formuser',  # or 'root' if you use the root user
    'password': 'password',  # replace with your MySQL password
    'host': 'localhost',
    'database': 'FormPractice'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
