from flask import Flask,render_template ,request,session,redirect,url_for
app = Flask(__name__,static_url_path='/static')

@app.route("/login",methods = ["POST","GET"])
def  login():
    if request.method == "POST":
        print("helloKJSEBCFL")
        user = request.form['username']
        password = request.form['secretkey']
        print(user)
        session['user']=user
        return render_template('user.html')
    else :
        print("hey")
        return render_template('index.html')

@app.route("/user")
def user():
    if "user" in session:
        user=session["user"]
        return render_template('user.html')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

def create_engine_models():
    DATABASE_URI = 'mysql+pymysql://avsd:helloworld@localhost:3306/college'
    engine = create_engine(DATABASE_URI,echo = True)
    Base.metadata.create_all(engine)

from project.mod_student import models,controllers
from project.mod_faculty import models,controllers

#create_engine_models()
