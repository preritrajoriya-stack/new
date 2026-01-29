from flask import Flask,render_template,redirect,request,url_for,flash
import mysql.connector


app_new = Flask(__name__)
app_new.secret_key = "secret123"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="user_auth_db"
    )

@app_new.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if not username or not email or not password:
            flash("All fields are required")
            return redirect(url_for("signup"))
        
        flash("Signup successful! Please login.", "success")
            
        
    return render_template("signup.html")

@app_new.route("/", methods=["GET", "POST"])
@app_new.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if not email or not password:
            flash("All fields are required")
            return redirect(url_for("login"))
        
        flash("Something went wrong")
    
    return render_template("login.html")

if __name__ == "__main__":
    app_new.run(debug=True)
    