from flask import Flask
from config import development
import sqlalchemy as db




engine = db.create_engine('sqlite:///database.sqlite')
connection = engine.connect()
metadata = db.MetaData()
shemas = db.Table('product', metadata, autoload=True, autoload_with=engine)
query = db.select([shemas])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()





app=Flask(__name__)

@app.route("/")
def index():
    return str(ResultSet)