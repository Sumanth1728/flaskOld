from datetime import date

today = date.today()
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
print(dt_string)


# Textual month, day and year


# Now that the table has been created by running
# BasicModelApp and SetUpDatabase we can play around with CRUD commands
# This is just an overview, usually we won't run a single script like this
# Our goal here is to just familiarize ourselves with CRUD commands

from tables import db, B_Admin ,B_Employee ,B_Customer,B_Customer_transactions,B_Customer_Card_Details,CardRequests,logs,CardDeActLogs
"""
cust=B_Customer.query.filter_by(C_id="C1").first()
cust1=cust
cust1.C_name="Jaya Chandra"
db.session.add(cust1)
db.session.commit()


cuslast = B_Customer.query.filter_by(C_id="C6").all()
for i in cuslast:
    print(i.C_name)

cusid='C'+str(int(Emplast.C_id[1:])+1)
cus1=B_Customer(cusid,"Revanth",22,"Revanth@gmail.com","USA",9879543221,"password",20200)
db.session.add(cus1)
db.session.commit()
"""
###########################
###### CREATE ############
#########################
db.create_all()

admin1=B_Admin(A_id="A1",A_pass="password")
db.session.add(admin1)
db.session.commit()

emp=B_Employee("E1","sumanth","Pasupuleti","Male",22,"s@gmail.com","vijayawada",9638521478,"password")

cus1=B_Customer("C1","JC","Dodda","Male",22,"jc@gmail.com","USA",9876543221,"password",20200)
cus2=B_Customer("C2","Reavnth","Posina","Male",22,"Revanth@gmail.com","Vijaywada",9876543871,"password",200000)

db.session.add(emp)
db.session.add(cus1)
db.session.add(cus2)
db.session.commit()

card1=B_Customer_Card_Details(C_id="C1", Card_Type="MasterCard", Card_No=456484560001, Card_Activate=True,Usagetype="Domestic",Card_Status_Type="Debit",ExpiryDate="02/23")
db.session.add(card1)
tarns=B_Customer_transactions(T_id="RF7609800001",C_id="C1",R_id="C2",Card_Number=456484560001,T_amount=1,T_Type="Debited",T_balance="1999",T_Time=str(dt_string))
tarns1=B_Customer_transactions(T_id="RF7609800001",C_id="C2",R_id="C1",Card_Number=0,T_amount=1,T_Type="Credited",T_balance="2001",T_Time=str(dt_string))
Cardn=CardRequests(C_id="C1", Card_Type="Visa",Card_Status_Type="Debit",Usagetype="International", Request_Status="Processing")
from sqlalchemy import DDL
from sqlalchemy import event
db.session.add(Cardn)
db.session.commit()
event.listen(
    CardRequests.__table__,
    "after_create",
    DDL("ALTER TABLE CardRequests SET id = 85000001 WHERE id=1;")
)
req=CardDeActLogs(C_id="C1",CardNo=456484560001,DeActReason="Lost")
db.session.add(req)
db.session.commit()
event.listen(
    CardDeActLogs.__table__,
    "after_create",
    DDL("ALTER TABLE CardDeActLogs SET id = 24000001 WHERE id=1;")
)
log=logs(Actor_id="A1",Actor_Type="Admin",ActionDone="Created a New Customer",OtherId="C1",ActionTime=dt_string)
db.session.add(log)
log0=logs(Actor_id="A1",Actor_Type="Admin",ActionDone="Created a New Customer",OtherId="C1",ActionTime=dt_string)
db.session.add(log0)
log1=logs(Actor_id="A1",Actor_Type="Admin",ActionDone="Created a New Employee ",OtherId="E1",ActionTime=dt_string)
db.session.add(log1)
db.session.add(tarns)
db.session.add(tarns1)
db.session.commit()



employee=B_Employee.query.all()
print(employee)
customer=B_Customer.query.all()
print(customer)
