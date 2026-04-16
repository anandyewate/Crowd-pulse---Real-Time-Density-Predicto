from flask import Flask, jsonify, request, session, redirect, url_for, render_template, flash
from flask_cors import CORS
from alert import get_alert, get_timeline
from models import init_db, create_user, verify_user
from sms_service import send_sms
from config import SECRET_KEY, CAMERAS
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app)

# Initialize Database
if not os.path.exists("users.db"):
    init_db()

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session.get("username"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = verify_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["phone_number"] = user["phone_number"]
            
            # Send SMS Alert
            send_sms(user["phone_number"], f"stampede risk at {CAMERAS[0]['id']} location")
            
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials! Try again.")
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        phone = request.form.get("phone")
        
        if create_user(username, password, phone):
            flash("Signup successful! Please login.")
            return redirect(url_for("login"))
        else:
            flash("Username already exists!")
            
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/alert")
def alert():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(get_alert())

@app.route("/timeline")
def timeline():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(get_timeline())

if __name__ == "__main__":
    app.run(debug=True)