import sqlite3
from flask import Flask,render_template,request,redirect
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
     
           
app.run()
