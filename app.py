from flask import Flask,render_template,request
from config import development
import sqlite3

app=Flask(__name__)





@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home(karbar=None):
        if not karbar==None:
            conn=sqlite3.connect('database.sqlite')
            cur = conn.cursor()
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()   
            cur.close()
            conn.close()
            print(karbar)
            username=findname(karbar)
            return render_template("full-screen-table.html",data=rows,user=username)
        else:
            conn=sqlite3.connect('database.sqlite')
            cur = conn.cursor()
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()   
            cur.close()
            conn.close()
            
            return render_template("full-screen-table.html",data=rows,user="کاربر")

@app.route("/compact")
def compact():
        conn=sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT * FROM product")
        rows = cur.fetchall()   
        cur.close()
        conn.close()
        return render_template("compact-table.html",data=rows)

    


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
                    return home(username)




    return render_template("index.html",status="1")

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


@app.route("/product",methods=["GET","POST"])
def product():
    bookname=request.form.get("bookname")
    writer=request.form.get("writer")
    gorooh=request.form.get("gorooh")
    boxindex=request.form.get("boxindex")
    count=request.form.get("count")
    price=request.form.get("price")
    discount=request.form.get("discount")
    regby=request.form.get("regby")
    barcode=request.form.get("barcode")
    
    try:
        sqliteConnection = sqlite3.connect('database.sqlite')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = f"""INSERT INTO product
                            (bookname, writer, gorooh, boxindex, count,price,discount,regby,barcode) 
                            VALUES 
                            ('{bookname}','{writer}','{gorooh}','{boxindex}',{count},{price},{discount},'{regby}','{barcode}')"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()
        return render_template("home.html",data=update())

    except sqlite3.Error as error:
          print("Failed to insert data into sqlite table", error)
    finally:
          if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")



    return render_template("product.html")
 
    

def update():
    conn=sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT * FROM product")
    rows = cur.fetchall()   
    cur.close()
    conn.close()
    return rows



def findname(username):
    conn=sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute(f"SELECT fname FROM users WHERE username='{username}'")
    fname = cur.fetchone()   
    tempfname=fname[0]
    cur.close()
    conn.close()
    conn=sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute(f"SELECT lname FROM users WHERE username='{username}'")
    lname = cur.fetchone()  
    templname=lname[0] 
    cur.close()
    conn.close()
    fnmaelname=tempfname+"    "+templname
    return fnmaelname







if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)