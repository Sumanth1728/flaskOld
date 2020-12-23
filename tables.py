from basecong import db
#####################################
####################################
###################################

# Let's create our first model!
# We inherit from db.Model class



class B_Admin(db.Model):


    __tablename__ = 'B_Admin'

    A_id = db.Column(db.Text,primary_key=True)

    A_pass=db.Column(db.Text)

    def __init__(self,A_id,A_pass):
        self.A_id=A_id
        self.A_pass=A_pass


    def __repr__(self):
        #
        return f"admin{self.A_id} fetched and password = {self.A_pass}"


######################################################################################################################################
########################################################################################################################################



class B_Employee(db.Model):

    # If you don't provide this, the default table name will be the class name
    __tablename__ = 'B_Employee'
    __table_args__ = {'extend_existing': True}

    # Now create the columns
    # Lots of possible types. We'll introduce through out the course
    # Full docs: http://docs.sqlalchemy.org/en/latest/core/types.html

    #########################################
    ## CREATE THE COLUMNS FOR THE TABLE ####
    #######################################

    # Primary Key column, unique id for each puppy
    E_id = db.Column(db.Text,primary_key=True)
    E_firstname = db.Column(db.Text)
    E_lastname = db.Column(db.Text)
    E_gender = db.Column(db.Text)
    E_age = db.Column(db.Integer)
    E_email=db.Column(db.Text,unique=True)
    E_address=db.Column(db.Text)
    E_number = db.Column(db.Integer)
    E_pass=db.Column(db.Text)

    # This sets what an instance in this table will have
    # Note the id will be auto-created for us later, so we don't add it here!
    def __init__(self,E_id,firstname,lastname,gender,age,email,address,number,E_pass):

        self.E_id = E_id
        self.E_firstname =firstname
        self.E_lastname = lastname
        self.E_gender = gender
        self.E_age = age
        self.E_email=email
        self.E_address=address
        self.E_number=number
        self.E_pass=E_pass


    def __repr__(self):

        # This is the  representation of B_Employee  in the model


        return f"employee fetched"





######################################################################################################################################
########################################################################################################################################






class B_Customer(db.Model):

    __tablename__ = 'B_Customer'
    __table_args__ = {'extend_existing': True}
    C_id = db.Column(db.Text,primary_key=True)
    C_firstname = db.Column(db.Text)
    C_lastname = db.Column(db.Text)
    C_gender = db.Column(db.Text)
    C_age = db.Column(db.Integer)
    C_email=db.Column(db.Text,unique=True)
    C_address=db.Column(db.Text)
    C_number = db.Column(db.Integer)
    C_pass=db.Column(db.Text)
    C_balance=db.Column(db.Float)
    C_Cards = db.relationship('B_Customer_Card_Details',backref='B_Customer',lazy='dynamic')
    C_Transacs = db.relationship('B_Customer_transactions',backref='B_Customer',lazy='dynamic')


    def __init__(self,C_id,firstname,lastname,gender,age,email,address,number,C_pass,balance):

        self.C_id = C_id
        self.C_firstname = firstname
        self.C_lastname = lastname
        self.C_gender = gender
        self.C_age = age
        self.C_email=email
        self.C_address=address
        self.C_number=number
        self.C_pass=C_pass
        self.C_balance=balance


    def __repr__(self):

        return f"customer fetched"





######################################################################################################################################
########################################################################################################################################




class B_Customer_transactions(db.Model):
    __tablename__ = 'B_Customer_transactions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True)
    T_id = db.Column(db.Integer)
    C_id = db.Column(db.Text,db.ForeignKey('B_Customer.C_id'))
    R_id=db.Column(db.Text)
    Card_Number=db.Column(db.Integer,db.ForeignKey('B_Customer_Card_Details.Card_No'))
    T_amount=db.Column(db.Float)
    T_Type=db.Column(db.Text)
    T_Time=db.Column(db.Text)
    T_balance=db.Column(db.Integer)


    def __init__(self,C_id,R_id,Card_Number,T_amount,T_Type,T_id,T_Time,T_balance):


        self.C_id = C_id
        self.T_id = T_id
        self.Card_Number=Card_Number
        self.T_amount=T_amount
        self.T_Type=T_Type
        self.R_id=R_id
        self.T_Time=T_Time
        self.T_balance=T_balance


    def __repr__(self):
        return [self.id,self.C_id,self.self.T_id,self.Card_Number,self.T_amount,self.T_Type,self.R_id]



######################################################################################################################################
########################################################################################################################################




class B_Customer_Card_Details(db.Model):

    __tablename__ = 'B_Customer_Card_Details'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True)
    C_id = db.Column(db.Text,db.ForeignKey('B_Customer.C_id'))
    Card_Type = db.Column(db.Text)
    Card_No = db.Column(db.Integer,unique=True)
    Usagetype=db.Column(db.Text)
    Card_Status_Type=db.Column(db.Text)
    ExpiryDate=db.Column(db.Text)
    Card_Activate=db.Column(db.Boolean)
    # add Expiry date to card details
    #add access type to card details
    Transacs = db.relationship('B_Customer_transactions',backref='B_Customer_Card_Details',lazy='dynamic')



    def __init__(self,C_id,Card_Type,Card_No,Card_Activate,Usagetype,Card_Status_Type,ExpiryDate):

        self.C_id = C_id
        self.Card_Type = Card_Type
        self.Card_No=Card_No
        self.Card_Activate=Card_Activate
        self.Card_Status_Type=Card_Status_Type
        self.ExpiryDate=ExpiryDate
        self.Usagetype=Usagetype


    def __repr__(self):
        return [self.id,self.self.self.self.C_id,self.self.self.Card_Type,self.self.Card_No,self.Card_Activate]


class CardRequests(db.Model):

    __tablename__ = 'CardRequests'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True)
    C_id = db.Column(db.Text,)
    Card_Type = db.Column(db.Text)
    Usagetype=db.Column(db.Text)
    Card_Status_Type=db.Column(db.Text)
    Request_Status=db.Column(db.Text)
    # add Expiry date to card details
    #add access type to card details

    def __init__(self,C_id,Card_Type,Usagetype,Card_Status_Type,Request_Status):

        self.C_id = C_id
        self.Card_Type = Card_Type
        self.Card_Status_Type=Card_Status_Type
        self.Usagetype=Usagetype
        self.Request_Status=Request_Status


    def __repr__(self):
        return "Card Created"


class logs(db.Model):
    __tablename__ = 'logs'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True)
    Actor_id = db.Column(db.Text)
    Actor_Type = db.Column(db.Text)
    ActionDone = db.Column(db.Text)
    OtherId=db.Column(db.Text)
    ActionTime=db.Column(db.Text)

    def __init__(self,Actor_id,Actor_Type,ActionDone,OtherId,ActionTime):

        self.Actor_id = Actor_id
        self.Actor_Type = Actor_Type
        self.ActionDone=ActionDone
        self.OtherId=OtherId
        self.ActionTime=ActionTime

class CardDeActLogs(db.Model):
    __tablename__ = 'CardDeActLogs'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True)
    C_id = db.Column(db.Text)
    CardNo = db.Column(db.Integer,unique=True)
    DeActReason = db.Column(db.Text)

    def __init__(self,C_id,CardNo,DeActReason):
        self.C_id = C_id
        self.CardNo = CardNo
        self.DeActReason=DeActReason

#creating Table instances
db.create_all()
