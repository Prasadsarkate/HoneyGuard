from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
import os, json

app = Flask(__name__)
app.secret_key = "supersecretkey"   # change this for production
socketio = SocketIO(app)

# -------- Dummy credentials (change to DB or config later) --------
ADMIN_EMAIL = "admin@honeyguard.com"
ADMIN_PASSWORD = "secure123"

# -------- Routes --------

@app.route("/", methods=["GET"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session["user"] = email
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------- Alerts API --------
@app.route("/api/alerts")
def api_alerts():
    alerts_file = "logs/alerts.log"
    if not os.path.exists(alerts_file):
        return jsonify([])
    with open(alerts_file, "r") as f:
        lines = f.readlines()
    alerts = [json.loads(l.strip()) for l in lines if l.strip()]
    return jsonify(alerts)

# -------- Socket.IO event for new alerts --------
def push_alert(alert):
    socketio.emit("new_alert", alert)

# Example: test alert push (can be removed later)
@app.route("/test_alert")
def test_alert():
    sample = {
        "timestamp": "2025-09-05 12:00:00",
        "level": "ALERT",
        "file": "honeypot.txt",
        "action": "deleted",
        "ip": "192.168.1.5",
        "user": "attacker",
        "process": "explorer.exe",
        "pid": 1234,
        "message": "File deleted → honeypot.txt"
    }
    push_alert(sample)
    return "Test alert sent!"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
