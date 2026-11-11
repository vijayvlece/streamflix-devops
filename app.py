import os, sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
BASE=os.path.dirname(os.path.abspath(__file__))
DB_PATH=os.environ.get("DATABASE_PATH",os.path.join(BASE,"streamflix.db"))
app=Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY","dev-only-change-this-secret")
def db():
 c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_db():
 with db() as c:
  c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)")
def login_required(fn):
 @wraps(fn)
 def wrapped(*a,**kw):
  if "user_id" not in session: return redirect(url_for("login"))
  return fn(*a,**kw)
 return wrapped
MOVIES=[
 {"title":"The Last Horizon","genre":"Sci-Fi","year":2025,"description":"A crew searches for a new home beyond the stars."},
 {"title":"Midnight Chase","genre":"Thriller","year":2024,"description":"One night. One city. A race against time."},
 {"title":"Ocean of Dreams","genre":"Drama","year":2023,"description":"A family discovers courage on a coastal journey."},
 {"title":"Code Red","genre":"Action","year":2025,"description":"A security team must stop a global cyber threat."},
 {"title":"Little Big Adventures","genre":"Family","year":2022,"description":"An unlikely team sets out on a joyful adventure."},
 {"title":"Hidden Truth","genre":"Mystery","year":2024,"description":"A small clue reveals a much bigger mystery."}]
@app.route("/")
def home(): return render_template("index.html",movies=MOVIES,username=session.get("username"))
@app.route("/health")
def health(): return {"status":"healthy","service":"streamflix"},200
@app.route("/register",methods=["GET","POST"])
def register():
 if request.method=="POST":
  username=request.form.get("username","").strip(); password=request.form.get("password","")
  if len(username)<3 or len(password)<8:
   flash("Username must be 3+ characters and password 8+ characters."); return render_template("register.html")
  try:
   with db() as c:
    cur=c.execute("INSERT INTO users(username,password_hash) VALUES (?,?)",(username,generate_password_hash(password)))
    session["user_id"]=cur.lastrowid; session["username"]=username
   return redirect(url_for("home"))
  except sqlite3.IntegrityError: flash("That username is already registered.")
 return render_template("register.html")
@app.route("/login",methods=["GET","POST"])
def login():
 if request.method=="POST":
  username=request.form.get("username","").strip(); password=request.form.get("password","")
  with db() as c: user=c.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone()
  if user and check_password_hash(user["password_hash"],password):
   session["user_id"]=user["id"]; session["username"]=user["username"]; return redirect(url_for("home"))
  flash("Invalid username or password.")
 return render_template("login.html")
@app.route("/logout")
def logout(): session.clear(); return redirect(url_for("home"))
init_db()
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT","5000")))
