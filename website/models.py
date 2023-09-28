#from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, validators, SubmitField

db = SQLAlchemy()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


""" class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') """


class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(16), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    idtype = db.Column(db.String(80), nullable=False)
    idno = db.Column(db.Integer, unique=True, nullable=False)
    passportno = db.Column(db.Integer, unique=True, nullable=False)
    nationality = db.Column(db.String(80), nullable=False)
    disability = db.Column(db.String(80), nullable=False)
    race = db.Column(db.String(24), nullable=False)
    employeeno = db.Column(db.Integer, unique=True, nullable=False)
    jobtitle = db.Column(db.String(240), nullable=False)
    phoneno = db.Column(db.Integer, unique=True, nullable=False)
    department = db.Column(db.String(80), nullable=False)
    municipality = db.Column(db.String(80), nullable=False)
    license = db.Column(db.String(24), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    def __init__(self, title, name, surname, idtype, idno, passportno, nationality, disability, race, employeeno, jobtitle, phoneno, department, municipality, license):
        self.title = title
        self.name = name
        self.surname = surname
        self.idtype = idtype
        self.idno = idno
        self.passportno = passportno
        self.nationality = nationality
        self.disability = disability
        self.race = race
        self.employeeno = employeeno
        self.jobtitle = jobtitle
        self.phoneno = phoneno
        self.department = department
        self.municipality = municipality
        self.license = license

    """ email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150)) """



class Questionnaire(Form):
    name = TextField('Name:',[validators.InputRequired()])
    surname = TextField('Surname:',[validators.InputRequired()])
    email = TextField('Email:',[validators.InputRequired(),validators.Email()])
    employeeNo = TextField('Employee No:',[validators.InputRequired()])
    height = TextField('Height (kg):',[validators.InputRequired()])
    feelings_options = [(1,'Bad'),(2,'OK'),(3,'Good')]
    #feelings = SelectField('Feelings about yourself:',coerce=int,choices=feelings_options, validators=[validators.InputRequired()])


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Knowledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tmanagement = db.Column(db.String(80), nullable=False)
    pmanagement = db.Column(db.String(80), nullable=False)
    interpersonal = db.Column(db.String(80), nullable=False)
    planning = db.Column(db.String(80), nullable=False)
    financial = db.Column(db.String(80), nullable=False)
    communication = db.Column(db.String(80), nullable=False)
    reportwriting = db.Column(db.String(80), nullable=False)
    projmanagement = db.Column(db.String(80), nullable=False)
    leadership = db.Column(db.String(80), nullable=False)
    diversity = db.Column(db.String(80), nullable=False)
    eq = db.Column(db.String(80), nullable=False)
    conflict = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    def __init__(self, tmanagement, pmanagement, interpersonal, planning, financial, communication, reportwriting, projmanagement, leadership, diversity, eq, conflict):
        self.tmanagement = tmanagement
        self.pmanagement = pmanagement
        self.interpersonal = interpersonal
        self.planning = planning
        self.financial = financial
        self.communication = communication
        self.reportwriting = reportwriting
        self.projmanagement = projmanagement
        self.leadership = leadership
        self.diversity = diversity
        self.eq = eq
        self.conflict = conflict

