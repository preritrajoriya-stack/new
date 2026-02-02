from flask import Flask, render_template, request, redirect, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "123456"  


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="prettt",
        database="user_auth_db"
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash("All fields are required")
            return redirect('/signup')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (username, email, hashed_password))
            conn.commit()

            flash("Signup successful! Please login.")
            return redirect('/login')

        except mysql.connector.Error as err:
            flash("Username or Email already exists")

        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                flash("Login successful!")
            else:
                flash("Invalid email or password")

        except Exception as e:
            flash("Something went wrong")

        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
