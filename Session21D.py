from Session21C import MongoDBHelper
from Session21A import User
from bson.objectid import ObjectId
import datetime
from tabulate import tabulate 
def main():
    print("WELCOME TO MONGODB TEST APP")
    dbHelper = MongoDBHelper()
    """
    user = User()
    user.add_user_details()
    document = vars(user)

    dbHelper.insert(document)
    """
    query= {"email":"john@gmail.com"}
    
    document_data_to_update = {"name": "john W", "age": 32, "created_on":datetime.datetime.now()}
    dbHelper.update(document=document_data_to_update, query=query)
    
    users = dbHelper.fetch()
    for user in users:
        print(user)



     








if __name__ == "__main__":
    main()



