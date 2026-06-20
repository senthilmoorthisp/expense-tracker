# Feature1 Branch Learning
# Expense Tracker Project
# New Advanced Expense Tracker
# Learning Git
import sqlite3
from flask import Flask,render_template,request,redirect,url_for
app=Flask(__name__)
conn=sqlite3.connect("expenses.db", check_same_thread=False)
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
 id INTEGER PRIMARY KEY,
 title TEXT,
 amount REAL,
 category TEXT)
""")
conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 username TEXT UNIQUE,
 password TEXT
 )
 """)
conn.commit()
@app.route("/register")
def register():
     return """
     <h2>Register</h2>
     <form method='POST' action='/save_user'>
     Username:<br>
     <input type='text' name='username'><br><br>
     Password:<br>
     <input type='password' name='password'><br><br>
     <button type='submit'>Register</button>
     </form>
     """
@app.route("/save_user", methods=["POST"])
def save_user():
    username=request.form["username"]
    password=request.form["password"]
    cursor.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",(username,password))
    conn.commit()
    return "User Registered Successfully"


@app.route("/")
def home():
    
    search=request.args.get("search")
    if search:
        cursor.execute("SELECT * FROM expenses WHERE title LIKE ?",('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM expenses")
    data=cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total=cursor.fetchone()[0]
    cursor.execute(""" SELECT category, SUM(amount) FROM expenses GROUP BY category""")
    summary=cursor.fetchall()
    return render_template("index.html",expenses=data,total=total,summary=summary)


@app.route("/add", methods=["POST"])
def add_expense():
    title=request.form["title"]
    amount=request.form["amount"]
    category=request.form["category"]
    cursor.execute(
    "INSERT INTO expenses(title,amount,category) VALUES(?,?,?)",(title,amount,category))
    conn.commit()
    return redirect("/")
@app.route("/delete/<int:id>")
def delete_expense(id):
    cursor.execute(
        "DELETE FROM expenses WHERE id=?",(id,))
    conn.commit()
    return redirect("/")
@app.route("/edit/<int:id>")
def edit_expense(id):
    cursor.execute(
        "SELECT * FROM expenses WHERE id=?",(id,))
    expense=cursor.fetchone()
    return f"""
    <h1>Edit Expense</h1>
    <form method='POST' action='/update/{expense[0]}'>
     Title:
     <input type='text' name='title' value='{expense[1]}'>
     <br><br>
     Amount:
     <input type='number' name='amount' value='{expense[2]}'>
     <br><br>
     Category:
     <input type='text' name='category' value='{expense[3]}'>
     <br><br>
     <button type='submit'>Update</button>
    </form>
    """
@app.route("/update/<int:id>",methods=["POST"])
def update_expense(id):
    title=request.form["title"]
    amount=request.form["amount"]
    category=request.form["category"]
    cursor.execute(
        """
        UPDATE expenses SET title=?, amount=?, category=? WHERE id=?""",(title,amount,category,id))
    conn.commit()
    return redirect("/")
     
           
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)
