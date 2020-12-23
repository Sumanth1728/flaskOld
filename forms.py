from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField,RadioField,SelectField,TextField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo,Length
class createcustomer(FlaskForm):
    firstname=StringField('First Name',validators=[DataRequired()])
    lastname=StringField('Lst Name',validators=[DataRequired()])
    gender=SelectField('Gender',choices=[('Male', 'Male'), ('Female', 'Female'),('Other', 'Other')],validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    phone=StringField('Phone Number',validators=[DataRequired()])
    balance=StringField('Current Desposited Amount')
    age=StringField('Age',validators=[DataRequired()])
    address=TextAreaField('Address',validators=[DataRequired()])
    submit=SubmitField("create")

class createemloyee(FlaskForm):
    firstname=StringField('First Name',validators=[DataRequired()])
    lastname=StringField('Lst Name',validators=[DataRequired()])
    gender=SelectField('Gender',choices=[('Male', 'Male'), ('Female', 'Female'),('Other', 'Other')],validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    phone=StringField('Phone Number',validators=[DataRequired()])
    age=StringField('Age',validators=[DataRequired()])
    address=TextAreaField('Address',validators=[DataRequired()])
    submit=SubmitField("create")

class searchform(FlaskForm):
    user=StringField('Enter Name or Email addrees ',validators=[DataRequired()])
    submit=SubmitField("Search")

class EditEmployee(FlaskForm):
    firstname=StringField('First Name')
    lastname=StringField('Lst Name')
    gender=SelectField('Gender',choices=[('Male', 'Male'), ('Female', 'Female'),('Other', 'Other')])
    phone=StringField('Phone Number')
    balance=StringField('Current Desposited Amount')
    age=StringField('Age')
    address=TextAreaField('Address')
    submit=SubmitField("Edit")

class RequestCards(FlaskForm):
    CardType=SelectField('Card Type',choices=[('Master Card', 'Master Card'), ('Visa', 'Visa'),('rupee', 'Other')])
    CardStatusType=SelectField('Card Status Type',choices=[('Debit Card', 'Debit Card'), ('Credit Card', 'Credit Card')])
    Usagetype=SelectField('Usagetype',choices=[('Domestic', 'Domestic'), ('International', 'International')])
    submit=SubmitField("Submit Request")

class AmountTransferForm(FlaskForm):
    Amount=StringField('Enter Amount of money to transfer',validators=[DataRequired()])
    submit=SubmitField("Transfer")

class EvaluationForm(FlaskForm):
    Approve=SubmitField("Approve")
    Decline=SubmitField("Decline")
