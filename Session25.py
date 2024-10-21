from flask import *
import datetime
from Session21C import MongoDBHelper
import hashlib

web_app= Flask("DOCTORs APP")
db_helper=MongoDBHelper()
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

@web_app.route("/home")
def home():
    if len(session["email"]) != 0:
        return render_template("home.html", name=session["name"], email=session["email"])
    else:
        return redirect("/")

@web_app.route("/success")
def success():
    return render_template("success.html" ,name=session['name'],email=session['email'])

web_app.route("/error")
def error():
    return render_template("error.html" ,name=session['name'],email=session['email'])

@web_app.route("/logout")
def logout():
    # Reset the Data in Session Object
    session["email"] = ""
    session["name"] = ""
    return redirect("/")

@web_app.route("/add-user", methods=["POST"])
def add_user_in_db():
    user_data= {
         "name": request.form["name"],
         "email": request.form["email"],
         "password": hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest(),
         "created_on": datetime.datetime.now(),
    }
    db_helper.collection = db_helper.db["users"]
    result=db_helper.insert(user_data)
   # message="Welcopme to Home Page. User id is {} ".format(result.inserted_id)
    session['user_id']=str(result.inserted_id)
    # session['name']=user_data["name"]
    #session['email']=user_data["email"]
    return render_template("home.html",email=session['email'])


@web_app.route("/fetch-user", methods=["POST"])
def feth_user_from_db():

    # Create a Dictionary with Data from HTML Register Form
    user_data = {
        "email": request.form["email"],
        "password": hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest(),
    }
    db_helper.collection = db_helper.db["users"]
    # Fetch user in DataBase i.e. MongoDB
    result = db_helper.fetch(query=user_data)
    print("result",result)
    

    #session['email']=user_data["email"]

    if len(result)>0:
         
         user_data=result[0]
         session['email']=user_data["email"]
         session['name']=user_data["name"]
         return render_template("home.html",name=session['name'], email=session['email'])
      
    else:
        return render_template("error.html",message="User Not Found. Please Try Again", name=session["name"], email=session["email"])
    


@web_app.route("/add-patient", methods=["POST"])    
def add_patient_in_db():
    patient_data= {
         "name": request.form["name"],
         "email": request.form["email"],
         "phone": request.form["phone"],
         "gender": request.form["gender"],
         "age":int(request.form["age"]),
         "address": request.form["address"],
         "doctor_email":session['email'],
         "doctor_name":session['name'],
         "created_on": datetime.datetime.now(),
    }
    db_helper.collection = db_helper.db["patients"]
    result=db_helper.insert(patient_data)
    return render_template("success.html", message = "Patient Added Successfully" ,name=session["name"], email=session["email"])
    

@web_app.route("/fetch-patients")
def fetch_patients_from_db():

    if len(session["email"])==0:
        return redirect("/")
    
    
    # Create a Dictionary with Data from HTML Register Form
    user_data = {
        "doctor_email": session["email"]
    }

    db_helper.collection = db_helper.db["patients"]
    # Fetch user in DataBase i.e. MongoDB
    result = db_helper.fetch(query=user_data)

   
    
    if len(result)>0:
        print(result)
        return render_template("patients.html", patients=result,name=session["name"], email=session["email"])
    else:
        return render_template("error.html",message="Patients Not Found. Please Try Again",name=session["name"], email=session["email"])

def main():
        
        web_app.secret_key= "doctors-app-key-v1"
        web_app.run()
    


if __name__=="__main__":
        main()