from flask import *
import datetime
from Session21C import MongoDBHelper
import hashlib

web_app= Flask("DOCTORs APP")
db=MongoDBHelper()
@web_app.route("/")


def index() :
    message = """<html>
    <head>
        <title>DOCTORs APP</title>
    </head>
    <body>
        <center>
            <h3>Welcome to DOCTORs APP</h3>
        </center>
    </body>
</html>"""
    return render_template("index.html")


@web_app.route("/register")
def register():
    return render_template("register.html")


@web_app.route("/add-user", methods=["POST"])
def add_user_in_db():
    user_data= {
         "name": request.form["name"],
         "email": request.form["email"],
         "password": hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest(),
         "created_on": datetime.datetime.now(),
    }

    result=db.insert(user_data)
   # message="Welcopme to Home Page. User id is {} ".format(result.inserted_id)
    session['user_id']=str(result.inserted_id)
    session['name']=user_data["name"]
    session['email']=user_data["email"]
    return render_template("home.html",email=session['email'])


@web_app.route("/fetch-user", methods=["POST"])
def feth_user_from_db():

    # Create a Dictionary with Data from HTML Register Form
    user_data = {
        "email": request.form["email"],
        "password": hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest(),
    }

    # Fetch user in DataBase i.e. MongoDB
    result = db.fetch(query=user_data)
    
    if len(result)>0:
         return render_template("home.html", email=session['email'])
    else:
        return "User Not Found. Please Try Again"

def main():
        
        web_app.secret_key= "doctors-app-key-v1"
        web_app.run()
    


if __name__=="__main__":
        main()