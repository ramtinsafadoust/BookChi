from flask import Flask,render_template,request ,  Response, redirect, url_for, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 

from config import development
import sqlite3
from flask_ngrok import run_with_ngrok

app=Flask(__name__)
run_with_ngrok(app)

app.config.update(

    SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id,username,password):
        self.id = id
        self.username=username
        self.password = password
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.username, self.password)


# create some users with ids 1 to 20
#
conn=sqlite3.connect('database.sqlite')
cur = conn.cursor() 
cur.execute("SELECT id FROM users")
id = cur.fetchall()   
cur.close()
conn.close()

conn=sqlite3.connect('database.sqlite')
cur = conn.cursor() 
cur.execute("SELECT username FROM users")
username = cur.fetchall()   
cur.close()
conn.close()

conn=sqlite3.connect('database.sqlite')
cur = conn.cursor() 
cur.execute("SELECT password FROM users")
password = cur.fetchall()   
cur.close()
conn.close()


for i in range (1,len(id)):
    users = User(id,username,password)












@app.route("/")
@login_required
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
            return render_template("full-screen-table.html",data=rows,usertus=username)
        else:

            return render_template("full-screen-table.html",data=update(),user=karbar)

@app.route("/compact")
@login_required
def compact():
        
        return render_template("compact-table.html",data=update(),user="کاربر")

    


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            
            conn=sqlite3.connect('database.sqlite')
            cur = conn.cursor() 
            
            cur.execute(f"SELECT password FROM users WHERE username='{username}';")
            
            dbpass = cur.fetchone() 
            print(dbpass)
            print(password)
            print(dbpass[0])
            cur.close()
            conn.close()
            if password == dbpass[0]:
                return render_template("full-screen-table.html",data=update(),user=username)
            else:
                abort(401)
     
        except :
            return "DB PROBLEM"
        
    else:
        return render_template("login.html")
  



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(id,username,password):
    return User(id,username,password)
    


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
        return render_template("full-screen-table.html",data=update())

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
      app.run()