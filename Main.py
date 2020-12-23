
from flask import Flask, render_template, session, redirect, url_for, session,flash,request
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired
from tables import db, B_Admin ,B_Employee ,B_Customer,B_Customer_transactions,B_Customer_Card_Details,CardRequests,logs,CardDeActLogs
from datetime import datetime
from basecong import app,mail
from flask_mail import *
from forms import createcustomer,searchform,EditEmployee,createemloyee,RequestCards,AmountTransferForm,EvaluationForm
# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
emid=0
class LoginForm(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    user = StringField('UserName',validators=[DataRequired()])
    passl  = StringField("Password",validators=[DataRequired()])
    submit = SubmitField('Submit')


##############################################
#############Login #########################3
#############################################
@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = LoginForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():


        # Grab the data from the breed on the form.

        m=form.user.data
        n=form.passl.data


        try:
            Admin1 = B_Admin.query.filter_by(A_id=form.user.data).first()
            print("A")
            if(Admin1.A_pass==form.passl.data):
                return redirect(url_for("admin",id=m))
            else:
                return "username and pasword doesn't match"

        except Exception as e:
            try:
                Emp1 = B_Employee.query.filter_by(E_id=form.user.data).first()
                if(Emp1.E_pass==form.passl.data):
                    return redirect(url_for("employee",id=m))

                else:
                    return "username and pasword doesn't match"

            except Exception as e:

                try:
                    cmp1 = B_Customer.query.filter_by(C_id=form.user.data).first()
                    if(cmp1.C_pass==form.passl.data):
                        return redirect(url_for("customer",id=m))

                    else:

                        return "username and pasword doesn't match"

                except Exception as e:


                    return(e)


    return render_template('index.html', form=form)


##############################################
#############Admin ##########################
#############################################

@app.route('/admin/<id>', methods=['GET', 'POST'])
def admin(id):

    return render_template('admin.html',id=id)

@app.route('/<Acctype>/<id>/CreateCustomer', methods=['GET', 'POST'])
def CreateCustomer(id,Acctype):
    form=createcustomer()
    if form.validate_on_submit():
        print("entered validate")
        cuslast = B_Customer.query.all()[-1]
        cusid="C"+str(int(cuslast.C_id[1:])+1)
        cus1=B_Customer(C_id=cusid, firstname=form.firstname.data,lastname=form.lastname.data,gender=form.gender.data, age=form.age.data, email=form.email.data, address=form.address.data, number=form.phone.data, C_pass="password", balance=form.balance.data)
        db.session.add(cus1)
        db.session.commit()
        cardno=B_Customer_Card_Details.query.all()[-1]
        cardid=cardno.Card_No+1
        card1=B_Customer_Card_Details(C_id=cusid, Card_Type="MasterCard", Card_No=cardid, Card_Activate=True,Usagetype="Domestic",Card_Status_Type="Debit",ExpiryDate="02/23")
        db.session.add(card1)
        now = datetime.now()
        dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
        log=logs(Actor_id=id,Actor_Type=Acctype,ActionDone="Created a New customer",OtherId=cusid,ActionTime=dt_string)
        db.session.add(log)
        db.session.commit()
        msg1="Customer Successfully Created"
        sub="Account Created"
        htmlbody=f"Hello <b>{form.firstname.data}</b>,<br><br>Your Account has been Created<br><b>Username</b> : {cusid}<br><b>Password</b> : password<br><br>please login to portal to find more<br>if not done by you please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
        msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[form.email.data])
        msg.html = htmlbody
        mail.send(msg)
        return render_template('CreateAlert.html',id=id,msg=msg1,Atype=Acctype)
    else:
        err=form.errors
        for i in err:
            flash(i+"-"+str(err[i]))

    return render_template('CreateNewCustomer.html',id=id,form=form,Acctype=Acctype)


@app.route('/admin/<id>/CreateEmployee', methods=['GET', 'POST'])
def CreateEmployee(id):
    form=createemloyee()
    if form.validate_on_submit():
        print("entered validate")
        emplast = B_Employee.query.all()[-1]
        empid="E"+str(int(emplast.E_id[1:])+1)
        print(empid)
        Emp1=B_Employee(E_id=empid, firstname=form.firstname.data,lastname=form.lastname.data,gender=form.gender.data, age=form.age.data, email=form.email.data, address=form.address.data, number=form.phone.data, E_pass="password")
        db.session.add(Emp1)
        now = datetime.now()
        dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
        log=logs(Actor_id=id,Actor_Type="Admin",ActionDone="Created a New Employee ",OtherId=empid,ActionTime=dt_string)
        db.session.add(log)
        db.session.commit()
        msg1="Employee Successfully Created"
        sub="Account Created"
        htmlbody=f"Hello <b>{form.firstname.data}</b>,<br><br>welcome to the Organization.we are glad that ypu are joining us<br>Your Account has been Created<br><b>Username</b> : {empid}<br><b>Password</b> : password<br><br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
        msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[form.email.data])
        msg.html = htmlbody
        mail.send(msg)
        return render_template('CreateAlert.html',id=id,msg=msg1,Atype="Admin")
    else:
        err=form.errors
        for i in err:
            flash(i+"-"+str(err[i]))
    return render_template('CreateNewEmployee.html',id=id,form=form)



@app.route('/<Acctype>/<id>/EditCustomer',methods=['GET', 'POST'])
def EditCustomer(id,Acctype):


    # Create instance of the form.
    form1 = searchform()

    # If the form is valid on submission (we'll talk about validation next)
    if form1.validate_on_submit():
        # Grab the data from the breed on the form.
        try:
            cust=B_Customer.query.filter_by(C_id=form1.user.data).first()
            return redirect(url_for("EditCustomerDetails",id=id,cid=cust.C_id,Acctype=Acctype))
        except Exception as e:
            try:
                cust=B_Customer.query.filter_by(C_email=form1.user.data).first()
                return redirect(url_for("EditCustomerDetails",id=id,cid=cust.C_id,Acctype=Acctype))
            except Exception as e:
                print(e)

    return render_template('EditCustomer.html',id=id,form1=form1,Acctype=Acctype)


@app.route('/<Acctype>/<id>/EditCustomerDeatils/<cid>',methods=['GET', 'POST'])
def EditCustomerDetails(id,cid,Acctype):

    form=EditEmployee()
    custm=B_Customer.query.filter_by(C_id=cid).first()

    if form.validate_on_submit():

        custm=B_Customer.query.filter_by(C_id=cid).first()
        if(form.firstname.data):
            custm.C_firstname=form.firstname.data
        if(form.lastname.data):
            custm.C_lastname=form.lastname.data
        if(form.gender.data):
            custm.C_gender=form.gender.data
        if(form.age.data):
            custm.C_age=form.age.data
        if(form.address.data):
            custm.C_address=form.address.data
        if(form.phone.data):
            custm.C_number=form.phone.data
        db.session.add(custm)
        now = datetime.now()
        dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
        log=logs(Actor_id=id,Actor_Type=Acctype,ActionDone="Edited Customer Details",OtherId=cid,ActionTime=dt_string)
        db.session.add(log)
        db.session.commit()
        sub="Account Details Edited"
        htmlbody=f"Hello <b>{custm.C_firstname}</b>,<br><br>Your Account Account Details  has been edited <br><b>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
        msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[custm.C_email])
        msg.html = htmlbody
        mail.send(msg)
        msg1="Customer Details Successfully Edited"
        return render_template('CreateAlert.html',id=id,msg=msg1,Atype=Acctype)
    else:
        err=form.errors
        for i in err:
            flash(i+"-"+str(err[i]))


    return render_template('EditCustomerDetails.html',id=id, form=form,custm=custm,Acctype=Acctype)






@app.route('/<Acctype>/<id>/SearchCustomer',methods=['GET', 'POST'])
def SearchCustomer(id,Acctype):

    cust= False
    cards1=False
    # Create instance of the form.
    form = searchform()

    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        m = form.user.data
        try:
            cust=B_Customer.query.filter_by(C_id=form.user.data).first()

            cards1=B_Customer_Card_Details.query.filter_by(C_id=cust.C_id).all()
        except Exception as e:
            try:
                cust=B_Customer.query.filter_by(C_email=form.user.data).first()
                cards1=B_Customer_Card_Details.query.filter_by(C_id=cust.C_id).all()
            except Exception as e:
                flash("No employee found with that Id or EmailID")


    return render_template('SearchCustomor.html',id=id, form=form, cust=cust,cards1=cards1,Acctype=Acctype)

@app.route('/admin/<id>/IssueCards',methods=['GET', 'POST'])
def IssueCards(id):
    reqs=CardRequests.query.all()

    return render_template('IssueCards.html',id=id,reqs=reqs)

@app.route('/admin/<id>/EvaluateIssueCardRequest/<rid>',methods=['GET', 'POST'])
def EvaluateIssueCardRequest(id,rid):
    reqs=CardRequests.query.filter_by(id=rid).first()
    cust=B_Customer.query.filter_by(C_id=reqs.C_id).first()
    form=EvaluationForm()
    if form.validate_on_submit():
        if form.Approve.data:
            cardno=B_Customer_Card_Details.query.all()[-1]
            cardid=cardno.Card_No+1
            card1=B_Customer_Card_Details(C_id=reqs.C_id, Card_Type= reqs.Card_Type, Card_No=cardid, Card_Activate=True,Usagetype=reqs.Usagetype ,Card_Status_Type=reqs.Card_Status_Type,ExpiryDate="02/28")
            db.session.add(card1)
            db.session.delete(reqs)
            now = datetime.now()
            dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
            log=logs(Actor_id=id,Actor_Type="Admin",ActionDone="Issue a new card for an customer ",OtherId=rid,ActionTime=dt_string)
            db.session.add(log)
            db.session.commit()
            sub="Card Approved"
            htmlbody=f"Hello <b>{cust.C_firstname}</b>,<br><br>Your Request for new Card is Approved <br><b>Reference Id</b> :{rid}<br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
            msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[cust.C_email])
            msg.html = htmlbody
            mail.send(msg)
            msg1="Issued a new card succesfully"
            return render_template('CreateAlert.html',id=id,msg=msg1,Atype="Admin")
        else:
            db.session.delete(reqs)
            now = datetime.now()
            dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
            log=logs(Actor_id=id,Actor_Type="Admin",ActionDone="Declined a Customer Request for new card ",OtherId=rid,ActionTime=dt_string)
            db.session.add(log)
            db.session.commit()
            sub="Card Declined"
            htmlbody=f"Hello <b>{cust.C_firstname}</b>,<br><br>Your Request for new Card is Declined  <br><b>Reference Id</b> :{rid}<br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
            msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[cust.C_email])
            msg.html = htmlbody
            mail.send(msg)
            msg="Declined a Customer Request for new card"
            return render_template('CreateAlert.html',id=id,msg=msg,Atype="Admin")
    else:
        flash(form.errors)

    return render_template('EvaluateIssueCardRequest.html',id=id,reqs=reqs,cust=cust,form=form)




@app.route('/<Acctype>/<id>/DeactivateCustomerCards',methods=['GET', 'POST'])
def DeactivateCustomerCards(id,Acctype):
    reqs=CardDeActLogs.query.all()

    return render_template('DeactivateCustomerCards.html',id=id,reqs=reqs,Acctype=Acctype)


@app.route('/<Acctype>/<id>/EvaluateDeactivateCardRequest/<rid>',methods=['GET', 'POST'])
def EvaluateDeactivateCardRequest(id,rid,Acctype):
    reqs=CardDeActLogs.query.filter_by(id=rid).first()
    cust=B_Customer.query.filter_by(C_id=reqs.C_id).first()
    form=EvaluationForm()
    if form.validate_on_submit():
        if form.Approve.data:
            card=B_Customer_Card_Details.query.filter_by(Card_No=reqs.CardNo).first()
            card.Card_Activate=False
            db.session.add(card)
            db.session.delete(reqs)
            now = datetime.now()
            dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
            log=logs(Actor_id=id,Actor_Type=Acctype,ActionDone="Accepted Customer Request for card Deactivation ",OtherId=rid,ActionTime=dt_string)
            db.session.add(log)
            db.session.commit()
            sub="Card Deactivation Request Approved"
            htmlbody=f"Hello <b>{cust.C_firstname}</b>,<br><br>Your Request for  Card Deactivation is Approved  <br><b>Reference Id</b> :{rid}<br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
            msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[cust.C_email])
            msg.html = htmlbody
            mail.send(msg)
            msg="Accepted Customer Request for card Deactivation"
            return render_template('CreateAlert.html',id=id,msg=msg,Atype=Acctype)
        else:

            db.session.delete(reqs)
            now = datetime.now()
            dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
            log=logs(Actor_id=id,Actor_Type=Acctype,ActionDone="Declined Customer Request for card Deactivation ",OtherId=rid,ActionTime=dt_string)
            db.session.add(log)
            db.session.commit()
            sub="Card Deactivation Request Declined"
            htmlbody=f"Hello <b>{cust.C_firstname}</b>,<br><br>Your Request for Card Deactivation is Declined  <br><b>Reference Id</b> :{rid}<br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
            msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[cust.C_email])
            msg.html = htmlbody
            mail.send(msg)
            msg="Declined Customer Request for card Deactivation"
            return render_template('CreateAlert.html',id=id,msg=msg,Atype=Acctype)
    else:
        flash(form.errors)

    return render_template('EvaluateDeactivateCardRequest.html',id=id,reqs=reqs,cust=cust,form=form,Acctype=Acctype)







@app.route('/<Acctype>/<id>/AddAmounttoCustomerAccount',methods=['GET', 'POST'])
def AddAmounttoCustomerAccount(id,Acctype):


    # Create instance of the form.
    form1 = searchform()

    # If the form is valid on submission (we'll talk about validation next)
    if form1.validate_on_submit():
        # Grab the data from the breed on the form.
        try:
            cust=B_Customer.query.filter_by(C_id=form1.user.data).first()
            return redirect(url_for("AddAmounttoCustomerAccount1",id=id,cid=cust.C_id,Acctype=Acctype))
        except Exception as e:
            try:
                cust=B_Customer.query.filter_by(C_email=form1.user.data).first()
                return redirect(url_for("AddAmounttoCustomerAccount1",id=id,cid=cust.C_id,Acctype=Acctype))
            except Exception as e:
                print(e)

    return render_template('AddAmounttoCustomerAccount.html',id=id,form1=form1,Acctype=Acctype)


@app.route('/<Acctype>/<id>/AddAmounttoCustomerAccount/<cid>',methods=['GET', 'POST'])
def AddAmounttoCustomerAccount1(id,cid,Acctype):

    form=AmountTransferForm()
    cust=B_Customer.query.filter_by(C_id=cid).first()

    if form.validate_on_submit():

        cust=B_Customer.query.filter_by(C_id=cid).first()
        cust.C_balance=cust.C_balance + int(form.Amount.data)
        db.session.add(cust)
        now = datetime.now()
        dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
        log=logs(Actor_id=id,Actor_Type=Acctype,ActionDone="Added Amount to customer Account ",OtherId=cid,ActionTime=dt_string)
        db.session.add(log)
        db.session.commit()
        sub=f"Amount Rs.{form.Amount.data} Credited into your Account"
        htmlbody=f"Hello <b>{cust.C_firstname}</b>,<br><br> An Amount of Rs.{form.Amount.data} credited into your Account  <br><br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
        msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[cust.C_email])
        msg.html = htmlbody
        mail.send(msg)
        msg="Succesfully Added Amount to the Customer Account"
        return render_template('CreateAlert.html',id=id,msg=msg,Atype=Acctype)
    else:
        print(form.errors)


    return render_template('AddAmounttoCustomerAccount1.html',id=id, form=form,cust=cust,Acctype=Acctype)



@app.route('/admin/<id>/Logs',methods=['GET', 'POST'])
def Logs(id):
    logss=logs.query.all()

    return render_template('Logs.html',id=id,logss=logss)






@app.route('/<Acctype>/<id>/EditEmployee',methods=['GET', 'POST'])
def EditEmployeee(id,Acctype):


    # Create instance of the form.
    form1 = searchform()

    # If the form is valid on submission (we'll talk about validation next)
    if form1.validate_on_submit():
        # Grab the data from the breed on the form.
        try:
            emp=B_Employee.query.filter_by(E_id=form1.user.data).first()
            return redirect(url_for("EditEmployeeDeatils",id=id,cid=emp.E_id,Acctype=Acctype))
        except Exception as e:
            try:
                cust=B_Employee.query.filter_by(E_email=form1.user.data).first()
                return redirect(url_for("EditEmployeeDeatils",id=id,cid=emp.E_id,Acctype=Acctype))
            except Exception as e:
                print(e)

    return render_template('EditCustomer.html',id=id,form1=form1,Acctype=Acctype)


@app.route('/<Acctype>/<id>/EditEmployeeDeatils/<cid>',methods=['GET', 'POST'])
def EditEmployeeDeatils(id,cid,Acctype):

    form=EditEmployee()
    custm=B_Employee.query.filter_by(E_id=cid).first()

    if form.validate_on_submit():

        custm=B_Employee.query.filter_by(E_id=cid).first()
        if(form.firstname.data):
            custm.E_firstname=form.firstname.data
        if(form.lastname.data):
            custm.E_lastname=form.lastname.data
        if(form.gender.data):
            custm.E_gender=form.gender.data
        if(form.age.data):
            custm.E_age=form.age.data
        if(form.address.data):
            custm.E_address=form.address.data
        if(form.phone.data):
            custm.E_number=form.phone.data
        db.session.add(custm)
        now = datetime.now()
        dt_string = now.strftime("%B %d %Y-- %H:%M:%S")
        log=logs(Actor_id=id,Actor_Type=Acctype,ActionDone="Edited Employee Details",OtherId=cid,ActionTime=dt_string)
        db.session.add(log)
        db.session.commit()
        sub="Account Details Edited"
        htmlbody=f"Hello <b>{custm.E_firstname}</b>,<br><br>Your Account Account Details  has been edited <br><b>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
        msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[custm.E_email])
        msg.html = htmlbody
        mail.send(msg)
        msg="Employee Details Successfully Edited"
        return render_template('CreateAlert.html',id=id,msg=msg,Atype=Acctype)
    else:
        err=form.errors
        for i in err:
            flash(i+"-"+str(err[i]))


    return render_template('EditEmployeeDetails.html',id=id, form=form,custm=custm,Acctype=Acctype)







##############################################
#############Employee ##########################
#############################################



@app.route('/employee/<id>', methods=['GET', 'POST'])
def employee(id):

    return render_template('employee.html',id=id)


@app.route('/Employee/<id>/AccountDetails', methods=['GET', 'POST'])
def EmployeeAccountDetails(id):
    try:
        cust=B_Employee.query.filter_by(E_id=id).first()
    except Exception as e:
        flash(e)

    return render_template('EmployeeAccountDetails.html',id=id,cust=cust)














##############################################
#############Customer ##########################
#############################################


@app.route('/customer/<id>', methods=['GET', 'POST'])
def customer(id):

    return render_template('customer.html',id=id)


@app.route('/customer/<id>/AccountDetails', methods=['GET', 'POST'])
def customerAccountDetails(id):
    try:
        cust=B_Customer.query.filter_by(C_id=id).first()
    except Exception as e:
        flash(e)

    return render_template('customerAccountDetails.html',id=id,cust=cust)




@app.route('/customer/<id>/CustomerCardDetails', methods=['GET', 'POST'])
def CustomerCardDetails(id):
    try:
        cust=B_Customer.query.filter_by(C_id=id).first()
        cards1=B_Customer_Card_Details.query.filter_by(C_id=id).all()

    except Exception as e:
        try:
            cust=B_Customer.query.filter_by(C_email=id).first()
            cards1=B_Customer_Card_Details.query.filter_by(C_id=id).all()

        except Exception as e:
            flash(e)

    return render_template('ViewCustomerCardDetails.html',id=id,cust=cust,cards1=cards1)


@app.route('/customer/<id>/RequestNewCard', methods=['GET', 'POST'])
def RequestNewCard(id):
    form = RequestCards()
    cust=B_Customer.query.filter_by(C_id=id).first()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        Cardn=CardRequests(C_id=id, Card_Type=form.CardType.data,Card_Status_Type=form.CardStatusType.data,Usagetype=form.Usagetype.data, Request_Status="Processing")
        db.session.add(Cardn)
        db.session.commit()
        sub="New Card Request Generated"
        htmlbody=f"Hello <b>{cust.C_firstname}</b>,<br><br>A request for new card is generated from your account  <br><b>Reference Id</b> :{Cardn.id}<br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
        msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[cust.C_email])
        msg.html = htmlbody
        mail.send(msg)
        msg="Your Request is submitted succesfully soon your staff will review your Request.Please check your email for futher Information"
        return render_template('CreateAlert.html',id=id,msg=msg,Atype="customer")

    return render_template('CustomerRequestNewCard.html',id=id,form=form)


@app.route('/customer/<id>/ViewCustomerTransactions', methods=['GET', 'POST'])
def ViewCustomerTransactions(id):
    try:
        cust=B_Customer_transactions.query.filter_by(C_id=id).all()

    except Exception as e:
        flash(e)

    return render_template('ViewCustomerTransactions.html',id=id,cust=cust)

@app.route('/customer/<id>/CustomerTransferFunds', methods=['GET', 'POST'])
def CustomerTransferFunds(id):
    form=searchform()

    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        if(id==form.user.data):
            flash("You can't enter your own id")
        else:
            try:
                cust=B_Customer.query.filter_by(C_id=form.user.data).first()
                return redirect(url_for("CustomerTransferFunds1",id=id,cid=cust.C_id))

            except Exception as e:
                try:
                    cust=B_Customer.query.filter_by(C_email=form.user.data).first()
                    return redirect(url_for("CustomerTransferFunds1",id=id,cid=cust.C_id))
                except AttributeError:
                    flash("The user Id Doesnot exist")



    return render_template('CustomerTransferFunds.html',id=id,form=form)


@app.route('/customer/<id>/CustomerTransferFunds1/<cid>', methods=['GET', 'POST'])
def CustomerTransferFunds1(id,cid):
    form=AmountTransferForm()
    cust=B_Customer.query.filter_by(C_id=cid).first()
    cust1=B_Customer.query.filter_by(C_id=id).first()

    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        if(cust1.C_balance< int (form.Amount.data)):
            flash("The amount exceeded the current balance in your account")
        else:
            cust.C_balance=cust.C_balance + int(form.Amount.data)
            cust1.C_balance=cust1.C_balance - int(form.Amount.data)
            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%B %d %Y-- %H:%M:%S")

            ts=B_Customer_transactions.query.all()[-1].T_id
            print(ts)

            tid=str(ts[0:3])+str(int(ts[3:])+1)
            tarns=B_Customer_transactions(T_id=tid,C_id=id,R_id=cid,Card_Number=0,T_amount=form.Amount.data,T_Type="Debited",T_balance=cust1.C_balance,T_Time=str(dt_string))
            tarns1=B_Customer_transactions(T_id=tid,C_id=cid,R_id=id,Card_Number=0,T_amount=form.Amount.data,T_Type="Credited",T_balance=cust.C_balance,T_Time=str(dt_string))
            db.session.add(cust)
            db.session.add(cust1)
            db.session.add(tarns)
            db.session.add(tarns1)
            db.session.commit()
            sub=f"Amount of {form.Amount.data} is Dredited from your Account "
            htmlbody=f"Hello <b>{cust1.C_firstname}</b>,<br><br>An Amount of Rs.{form.Amount.data} is Debited  from your account  <br><b>Reference Id</b> :{tid}<br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
            msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[cust1.C_email])
            msg.html = htmlbody
            mail.send(msg)
            sub=f"Amount of {form.Amount.data} is Credited into your Account "
            htmlbody=f"Hello <b>{cust.C_firstname}</b>,<br><br>Amount{form.Amount.data} is Credited into your Account <br><b>Reference Id</b> :{tid}<br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
            msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[cust.C_email])
            msg.html = htmlbody
            mail.send(msg)
            msg="Your Request is submitted succesfully .Please refer to your email for futher Details "
            return render_template('CreateAlert.html',id=id,msg=msg,Atype="customer")



    return render_template('CustomerTransferFunds1.html',id=id,cust=cust,form=form)


@app.route('/customer/<id>/CustomerBalanceEnquiry', methods=['GET', 'POST'])
def CustomerBalanceEnquiry(id):
    cust1=B_Customer.query.filter_by(C_id=id).first().C_balance
    return render_template('CustomerBalanceEnquiry.html',id=id,cust1=cust1)

@app.route('/customer/<id>/CustomerCardDeavtivateRequest', methods=['GET', 'POST'])
def CustomerCardDeavtivateRequest(id):
    cust=B_Customer.query.filter_by(C_id=id).first()
    cards=B_Customer_Card_Details.query.filter_by(C_id=id).all()
    a=[]
    for card in cards:
        print(card.Card_No)
        print(str(id)+"--"+str(card.Card_No)+"--"+ str(card.Card_Type)+"--"+str(card.Card_Status_Type) +"--"+str(card.Usagetype))
        a.append((card.Card_No , str(id)+"--"+str(card.Card_No)+"--"+ str(card.Card_Type)+"--"+str(card.Card_Status_Type) +"--"+str(card.Usagetype)))

    class AmountTransferForm(FlaskForm):
        card1=SelectField('Select the card',choices=a,validators=[DataRequired()])
        reason=StringField('Reason for Deactivation',validators=[DataRequired()])
        submit=SubmitField("Request")

    form=AmountTransferForm()
    if form.validate_on_submit():
        req=CardDeActLogs(C_id=id,CardNo=str(form.card1.data),DeActReason=form.reason.data)
        cust=B_Customer.query.filter_by(C_id=id).first()
        db.session.add(req)
        db.session.commit()
        sub=f"A request for card Deactivation is rised from your Account "
        htmlbody=f"Hello <b>{cust.C_firstname}</b>,<br><br>A request for card Deactivation is rised from your Account  <br><b>Reference Id</b> :{req.id}<br>please login to portal to find more<br>if not done on your request, please report us<br><b>Best Wishes,</b><br><br>Team Bank Application"
        msg = Message(sub, sender = 'bankapplication24@gmail.com', recipients=[cust.C_email])
        msg.html = htmlbody
        mail.send(msg)
        msg="Your Request is submitted succesfully soon your staff will review your Request.Please check your email for futher Information"
        return render_template('CreateAlert.html',id=id,msg=msg,Atype="customer")
    else:
        flash(form.errors)

    return render_template('CustomerCardDeavtivateRequest.html',id=id,form=form)













if __name__ == '__main__':
    app.run(debug=True)
