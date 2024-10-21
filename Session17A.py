import datetime

"""create table Consultation(
        cid int primary key auto_increment,
        pid int,
        remarks varchar(256),
        medicines varchar(256),
        next_followup datetime,
        created_on datetime,
        FOREIGN KEY (pid) REFERENCES Patient(pid)
        );
"""""

class Consultation:
    def __init__(self,pid=0,cid=0,remarks="",medicines="",next_followup =""):
        self.pid = pid
        self.cid = cid
        self.remarks = remarks
        self.medicines = medicines
        self.next_followup =next_followup 
        self.created_on = datetime.datetime.now()

    def add_consultation_details(self):
        self.pid = input("Enter pid: ")
        self.remarks = input("Enter consultation remarks: ")
        self.medicines = input("Enter medicines: ")
        self.next_followup = input("Enter next followup(yyyy-mm-dd hh-mm-ss): ")
        

    def show(self):
        print("~~~~~~~~~~~~CONSULTATION~~~~~~~~~~~~~")
        consultation=""" 
        {pid} | {cid} | 
        {remarks} | {medicines} |
        {next_followup} | {created_on}""".format_map(vars(self))
        print(consultation)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")              
