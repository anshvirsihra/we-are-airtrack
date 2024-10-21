
from Session17 import Patient
from Session17A import Consultation
from Session15A import Database
from tabulate import tabulate


def main():
    print("-------------------")
    print("WELCOME to DOCTOR's APP")
    print("-------------------")

    db = Database()

    while True:
        print("1: Add New patient")
        print("2: Update Existing patient")
        print("3: Delete Existing patient")
        print("4: View patient By Phone")
        print("5: View patient By CID")
        print("6: View All patient")
        print("7: Add Consultation For Patient")
        print("8: View All Consultations")
        print("9: View Consultations of a Patient")
        print("10: View FollowUps")
        print("0: To Quit App")

        choice = int(input("Enter Your Choice: "))

        if choice == 1:
            patient = Patient()
            patient.add_patient_details()
            sql = "insert into Patient values(null, '{name}', '{phone}', '{email}', '{dob}', '{gender}', '{created_on}')".format_map(vars(patient))

            # sql = "insert into Customer values(null, '{}', '{}', '{}', {}, '{}', null)".format(customer.name, customer.phone, customer.email, customer.age, customer.gender)

            db.write(sql)
            print("[CMS App]", patient.name, "Saved in DataBase")

        elif choice == 2:
            cid=input("enter your CID number:")
            sql="select * from Patient where cid = {}".format(cid)
            rows=db.read(sql)
            print(rows)
            customer =patient(cid=rows[0][0],name=rows[0][1],phone=rows[0][2],email=rows[0][3],dob=rows[0][4],gender=rows[0][5])
            
            print("patient to update:")
            patient.show()
            patient.update_patient_details()
            
            sql="update Patient set name = '{name}',phone  ='{phone}',email='{email}',dob={dob},gender='{gender}',created_on='{created_on}'  where cid = {cid}".format_map(vars(customer))

            db.write(sql)
            patient.show()


        elif choice == 3:
            cid = int(input("Enter patient ID to be Deleted: "))
            sql = "delete from Patient where cid = {}".format(cid)
            ask=input("are you sure you want to delete (yes/no):")
            if ask=="yes":
                db.write(sql)
                print("[CMS App]", cid, "Deleted from DataBase")
            else:
                 print("delete operation skipped")   
        
        elif choice == 4:
            phone=input("enter your phone number:")
            sql="select * from Patient where phone = '{}'".format(phone)
            rows=db.read(sql)
            columns=["cid","name","phone","email","dob","gender","created_on"]
            print(tabulate(rows,headers=columns,tablefmt='grid'))
        
        elif choice == 5:
            phone=input("enter your CID number:")
            sql="select * from Patient where phone = {}".format(cid)
            rows=db.read(sql)
            columns=["cid","name","phone","email","dob","gender","created_on"]
            print(tabulate(rows,headers=columns,tablefmt='grid'))
        
        elif choice == 6:
            sql="select * from Patient"
            rows=db.read(sql)
            columns=["cid","name","phone","email","dob","gender","created_on"]
            print(tabulate(rows,headers=columns,tablefmt='grid'))
        
        elif choice == 7:
            consultation = Consultation()
            consultation.add_consultation_details()
            sql = "insert into Consultation values(null, {pid}, '{remarks}', '{medicines}', '{next_followup}', '{created_on}')".format_map(vars(consultation))
            db.write(sql)
            print("Consultation Created..")
    
        elif choice == 8:
            sql = "select * from Consultation"
            rows = db.read(sql)

            columns = ["cid", "pid", "remarks", "medicines", "next_followup", "created_on"]  
            print(tabulate(rows, headers=columns, tablefmt='grid'))

        elif choice == 9:
            pid = int(input("Enter Patient ID: "))
            sql = "select * from Consultation where pid = {}".format(pid)
            rows = db.read(sql)

            columns = ["cid", "pid", "remarks", "medicines", "next_followup", "created_on"]    
            print(tabulate(rows, headers=columns, tablefmt='grid'))         

        elif choice == 10:
            start_date = input("Enter Start Date Time(yyyy-mm-dd hh:mm:ss): ")
            end_date = input("Enter End Date Time(yyyy-mm-dd hh:mm:ss): ")
            
            sql = "select * from Consultation where next_followup >= '{}' and next_followup <= '{}'".format(start_date, end_date)
            rows = db.read(sql)

            columns = ["cid", "pid", "remarks", "medicines", "next_followup", "created_on"]    
            print(tabulate(rows, headers=columns, tablefmt='grid'))     

        elif choice == 0:
            break
        
        else:
            print("[CMS APP] Invalid Choice", choice)


if __name__ == "__main__":
    main()
