import os
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.discord import make_discord_blueprint, discord
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import secrets

# Load environment variables from .env
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))

# Database setup (using DATABASE_URL from .env)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///logins.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Login Log Model
class LoginLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50))
    user_email = db.Column(db.String(150))
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Google OAuth Blueprint
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ],  # Now explicitly matches what Google returns
    redirect_to="google_login",
)
app.register_blueprint(google_bp, url_prefix="/login")

# Discord OAuth Blueprint
discord_bp = make_discord_blueprint(
    client_id=os.getenv("DISCORD_CLIENT_ID"),
    client_secret=os.getenv("DISCORD_CLIENT_SECRET"),
    scope=["identify", "email"],
    redirect_to="discord_login",
)
app.register_blueprint(discord_bp, url_prefix="/login")

# Function to check if IP is abusing the system
def is_ip_abusing(ip):
    time_limit = datetime.now(timezone.utc) - timedelta(minutes=10) # Look at last 10 minutes
    recent_logins = LoginLog.query.filter(LoginLog.ip_address == ip, LoginLog.timestamp > time_limit).count()
    return recent_logins > 5  # Adjust threshold as needed

@app.route("/")
def home():
    return '''
    <h1>Choose an authentication method:</h1>
    <a href="/login/google">Login with Google</a><br>
    <a href="/login/discord">Login with Discord</a>
    '''

@app.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    ip = request.remote_addr  # Get client IP
    if is_ip_abusing(ip):
        return "Too many login attempts. Try again later."

    resp = google.get("/oauth2/v1/userinfo")
    user_info = resp.json()

    # Log login
    login_event = LoginLog(provider="Google", user_email=user_info["email"], ip_address=ip)
    db.session.add(login_event)
    db.session.commit()

    return f"Logged in as {user_info['email']}"

@app.route("/discord")
def discord_login():
    if not discord.authorized:
        return redirect(url_for("discord.login"))

    ip = request.remote_addr  # Get client IP
    if is_ip_abusing(ip):
        return "Too many login attempts. Try again later."

    resp = discord.get("/api/users/@me")
    user_info = resp.json()

    # Log login
    login_event = LoginLog(provider="Discord", user_email=f"{user_info['username']}#{user_info['discriminator']}", ip_address=ip)
    db.session.add(login_event)
    db.session.commit()

    # Redirect to landing page with user info
    return redirect(url_for("landing_page", provider="Discord", username=f"{user_info['username']}#{user_info['discriminator']}"))

@app.route("/landing")
def landing_page():
    # Get query parameters
    provider = request.args.get("provider")
    username = request.args.get("username")

    # Render a landing page template
    return render_template("landing.html", provider=provider, username=username)


if __name__ == "__main__":
    app.run(debug=True, ssl_context=("../cert.pem", "../key.pem"))
