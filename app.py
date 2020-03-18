from flask import Flask,render_template
from config import development
import sqlite3

app=Flask(__name__)

conn=sqlite3.connect('database.sqlite')
cur = conn.cursor()
cur.execute("SELECT * FROM product")
rows = cur.fetchall()
for row in rows:
        print(row)


@app.route("/")
def index():
   
    return render_template("index.html",data=rows)