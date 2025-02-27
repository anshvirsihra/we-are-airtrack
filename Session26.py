"""
    Web Application Development with Flask
    https://flask.palletsprojects.com/en/3.0.x/

    1. Install Flask in Virtual Env
       pip install Flask

    2. Create Object of Flask

    3. Create a Function, with route as /

    4. In main function run the Flas App using run()

    5. Return the HTML webapge as a template from function
"""

from flask import *
import datetime
import hashlib
from Session21C import MongoDBHelper
from bson.objectid import ObjectId

# Create the Object of Flask
# Which represents a Web Application
web_app = Flask("Doctors App")
db_helper = MongoDBHelper()

@web_app.route("/") # Decorator
def index():

    # either you can return plain text
    # message = "Welcome to Patient Management System. Its {}".format(datetime.datetime.now())

    # OR you can return HTML
    message = """
    <html>
    <head>
        <title>Doctors App</title>
    </head>
    <body>
        <center>
            <h3>Welcome to Doctors Appm</h3>
        </center>
    </body>
    </html>
    """

    # return message

    # render_template is used to return web pages (html pages)
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
    return render_template("success.html", name=session["name"], email=session["email"])

@web_app.route("/error")
def error():
    return render_template("error.html", name=session["name"], email=session["email"])

@web_app.route("/logout")
def logout():
    # Reset the Data in Session Object
    session["email"] = ""
    session["name"] = ""
    return redirect("/")


@web_app.route("/add-user", methods=["POST"])
def add_user_in_db():

    # Create a Dictionary with Data from HTML Register Form
    user_data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "password": hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest(),
        "created_on": datetime.datetime.now()
    }

    db_helper.collection = db_helper.db["users"]
    # Save user in DataBase i.e. MongoDB
    result = db_helper.insert(user_data)
    # message = "Welcome to Home Page. User ID is: {}".format(result.inserted_id)
    # return message

    # Write the data in the Session Object
    # This data can now be used anywhere in the project
    session['name'] = user_data["name"]
    session['email'] = user_data["email"]

    # return render_template("home.html", name=session['name'], email=session['email'])
    return render_template("home.html", name=session['name'], email=session['email'])

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

    print("result:", result)
    
    if len(result)>0:
        user_data = result[0] # Get the dictionary from List 
        session['email'] = user_data["email"]
        session['name'] = user_data["name"]
        return render_template("home.html", name=session['name'], email=session['email'])
    else:
        return render_template("error.html", message="User Not Found. Please Try Again",
                               name=session["name"], email=session["email"])
    
    


@web_app.route("/add-patient", methods=["POST"])
def add_patient_in_db():

    # Create a Dictionary with Data from HTML Register Form
    patient_data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "gender": request.form["gender"],
        "age": int(request.form["age"]),
        "address": request.form["address"],
        "doctor_email": session['email'],
        "doctor_name": session['name'],
        "created_on": datetime.datetime.now()
    }

    db_helper.collection = db_helper.db["patients"]
    # Save Patient in DataBase i.e. MongoDB
    result = db_helper.insert(patient_data)
    return render_template("success.html", message = "Patient Added Successfully",
                           name=session["name"], email=session["email"])


@web_app.route("/update-patient/<id>")
def update_patient(id):
    print("Patinet to be updated:", id)
    
    # Save Patient ID in Session, which needs to be updated
    session["id"] = id
    
    # Fetch document from patient collection, where id matches
    query = {"_id": ObjectId(id)}
    db_helper.collection = db_helper.db["patients"]
    
    # result is a list
    result = db_helper.fetch(query=query)
    
    # As we will get the list of documents, and 0th index will be our document
    # with patient id matching the one we have passed
    patient_doc = result[0]

    return render_template("update-patient.html",
                           name=session["name"], 
                           email=session["email"], 
                           patient=patient_doc)


@web_app.route("/delete-patient/<id>")
def delete_patient(id):
    print("Patinet to be deleted:", id)
    query = {"_id": ObjectId(id)}
    db_helper.collection = db_helper.db["patients"]
    db_helper.delete(query)
    return render_template("success.html", message = "Patient Deleted Successfully",
                           name=session["name"], email=session["email"])


@web_app.route("/update-patient-in-db", methods=["POST"])
def update_patient_in_db():

    # Create a Dictionary with Data from HTML Register Form
    patient_data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "gender": request.form["gender"],
        "age": int(request.form["age"]),
        "address": request.form["address"],
        "doctor_email": session['email'],
        "doctor_name": session['name'],
        "created_on": datetime.datetime.now()
    }

    db_helper.collection = db_helper.db["patients"]

    query = {"_id": ObjectId(session["id"])}
    # Save Patient in DataBase i.e. MongoDB
    result = db_helper.update(patient_data, query)
    return render_template("success.html", message = "Patient Updated Successfully",
                           name=session["name"], email=session["email"])



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
    # result here, is a list of documents(dictionaries) from MongoDB
    
    if len(result)>0:
        print(result)
        return render_template("patients.html", patients=result, 
                               name=session["name"], email=session["email"])
    else:
        return render_template("error.html", message="Patients Not Found. Please Try Again",
                               name=session["name"], email=session["email"])


def main():

    # In order to use Session Tracking, create a Secret Key
    web_app.secret_key = "doctors-app-key-v1"

    # Run the App infinitely, till user wont quite
    web_app.run()
    # web_app.run(port=5001) # optionally you can give the port number

if __name__ == "__main__":
    main()