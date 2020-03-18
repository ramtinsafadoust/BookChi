from flask import Flask,render_template,request
from config import development
import sqlite3

app=Flask(__name__)





@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
        conn=sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT * FROM product")
        rows = cur.fetchall()   
        cur.close()
        conn.close()
        return render_template("home.html",data=rows)

    


@app.route('/login', methods=["POST"])
def login():
    username=request.form.get("username")
    
    password=request.form.get("password")
    
    if username and password:
    

            conn=sqlite3.connect('database.sqlite')
            cur = conn.cursor()
            cur.execute(f"SELECT password FROM users WHERE username='{username}'")
            rows = str(cur.fetchone() )
            print ("=========>> THIS IS ROWS"+str(rows))  
            temp=rows[2:-3]
            print ("=========>> THIS IS pass   "+str(password)+"THIS IS TEMp=========>"+str(temp) )  
            if password == temp:
                    conn=sqlite3.connect('database.sqlite')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM product")
                    rows = cur.fetchall()   
                    cur.close()
                    conn.close()
                    return render_template("home.html",data=rows,user=username)




    return render_template("index.html")

@app.route("/search",methods=["get"])
def search():
    data=   request.args.get("search")
    print(data)
    conn=sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    qur="SELECT * FROM product WHERE id LIKE "+"'%"+data+"%' OR bookname LIKE "+"'%"+data+"%'OR writer LIKE "+"'%"+data+"%' OR gorooh LIKE "+"'%"+data+"%' OR boxindex LIKE "+"'%"+data+"%'OR barcode LIKE "+"'%"+data+"%'"
    cur.execute(qur)
    searchrows=cur.fetchall()
    cur.close()
    conn.close()
    return render_template("search.html",data=searchrows)