import datetime
import hashlib
class User: 

    def __init__(self,name="",phone="",email="",password="",age=0,gender=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender
        self.created_on = datetime.datetime.now()
        
    def add_user_details(self): 
        self.name = input("Enter Customer Name: ")
        self.phone = input("Enter Customer Phone: ")
        self.email = input("Enter Customer Email: ")
        self.password =input("Enter Customer  Password: ").encode('utf-8')
        self.password = hashlib.sha256(self.password).hexdigest()


        self.age = int(input("Enter Customer Age: "))
        self.gender = input("Enter Customer Gender: ")

