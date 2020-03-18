from flask import Flask,render_template,request
from config import development
import sqlite3

app=Flask(__name__)

conn=sqlite3.connect('database.sqlite')
cur = conn.cursor()
cur.execute("SELECT * FROM product")
rows = cur.fetchall()





@app.route("/")
def index():
    return render_template("index.html",data=rows)


@app.route("/search",methods=["get"])
def search():
    data=   request.args.get("search")
    print(data)
    conn=sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    qur="SELECT * FROM product WHERE id LIKE "+"'%"+data+"%' OR bookname LIKE "+"'%"+data+"%'OR writer LIKE "+"'%"+data+"%' OR gorooh LIKE "+"'%"+data+"%' OR boxindex LIKE "+"'%"+data+"%'OR barcode LIKE "+"'%"+data+"%'"
    cur.execute(qur)
    searchrows=cur.fetchall()
    return render_template("search.html",data=searchrows)