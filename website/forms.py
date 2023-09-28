from wtforms import (
    StringField,
    SelectField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
)

from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp ,Optional
import email_validator
from flask_login import current_user
from wtforms import ValidationError,validators
from .models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Note, Personal, Upload
from . import db
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
import json
import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from io import BytesIO
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import RequestEntityTooLarge
from flask import Flask, abort, make_response, jsonify
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import phonenumbers
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError



class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    # Placeholder labels to enable form rendering
    username = StringField(
        validators=[Optional()]
    )

#(([0-9]{2})(0|1)([0-9])([0-3])([0-9]))([ ]?)(([0-9]{4})([ ]?)([0-1][8]([ ]?)[0-9])) regex id numbers
#'[A-Za-z]{2,25}||\s[A-Za-z]{2,25}' regex names
class register_form(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )

class PersonalForm(FlaskForm):
    title = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    name = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    surname = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    idtype = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    idno = IntegerField(validators=[
            InputRequired(),
            Length(13, message="Please provide a valid ID No"),
            Regexp(
                "^(([0-9]{2})(0|1)([0-9])([0-3])([0-9]))([ ]?)(([0-9]{4})([ ]?)([0-1][8]([ ]?)[0-9]))",
                0,
                "Invalid ID Number. Please try again",
            ),
        ]
    )
    passportno = StringField(validators=[
            InputRequired(),
            Length(13, message="Please provide a valid ID No"),
            Regexp(
                "^[A-Z][0-9]{8}",
                0,
                "The passport number must be in the following format: E58728453. It must start with a Capitol Letter followed by 8 digits",
            ),
        ]
    )
    nationality = SelectField(validators=[InputRequired(), Length(2,80, message = "Please make a selection")])
    disability = SelectField(validators=[InputRequired(), Length(2,80, message = "Please make a selection")])
    race = SelectField(validators=[InputRequired(), Length(2,80, message = "Please make a selection")])
    employeeno = IntegerField(validators=[
            InputRequired(),
            Length(13, message="Please provide a valid ID No"),
            Regexp(
                "^(72)[0][0-9]{6}$",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    jobtitle = SelectField(validators=[InputRequired(), Length(2,80, message = "Please make a selection")])
    phoneno = IntegerField(validators=[
            InputRequired(),
            Length(13, message="Please provide a valid ID No"),
            Regexp(
                "^(\+27|0)[6-8][0-9]{8}$",
                0,
                "Not a valid phone numnber. Please try again!",
            ),
        ]
    )
    """ phoneno = StringField('Phone', validators=[InputRequired()]) """
    department = SelectField(validators=[InputRequired(), Length(2,80, message = "Please make a selection")])
    municipality = SelectField(validators=[InputRequired(), Length(2,80, message = "Please make a selection")])
    license = SelectField(validators=[InputRequired(), Length(2,80, message = "Please make a selection")])
    submit = SubmitField('submit')

    def validate_phoneno(self, phoneno):
        try:
            p = phonenumbers.parse(phoneno.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

    def validate_idno(self, idno):
        if User.query.filter_by(idno=idno.data).first():
            raise ValidationError("ID No already registered!")

    def validate_passportno(self, passportno):
        if User.query.filter_by(passportno=passportno.data).first():
            raise ValidationError("Passport number belongs to someone else!")
    
    def validate_employeeno(self, employeeno):
        if User.query.filter_by(employeeno=employeeno.data).first():
            raise ValidationError("Employee number belongs to someone else!")
    
    def validate_phoneno(self, phoneno):
        if User.query.filter_by(phoneno=phoneno.data).first():
            raise ValidationError("Phone number belongs to someone else!")


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")


class KnowledgeForm(FlaskForm):
    tmanagement = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    pmanagement = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    interpersonal = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    planning = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    financial = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    communication = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    reportwriting = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    projmanagement = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    leadership = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    diversity = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    eq = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    conflict = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])


class TrainingForm(FlaskForm):
    tmanagement = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    pmanagement = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    interpersonal = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    planning = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    financial = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    communication = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    reportwriting = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    projmanagement = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    leadership = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    diversity = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    eq = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    conflict = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])


class QualDetailsForm(FlaskForm):
    qual1name = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    level1 = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    achievetype1 = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    qual1surname = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    institution1 = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    qual1status = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    qual2name = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    level2 = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    achievetype2 = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    qual2surname = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    institution2 = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    qual2status = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    qual3name = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    level3 = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    achievetype3 = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    qual3surname = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    institution3 = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    qual3status = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])


class FundingForm(FlaskForm):
    fundedqual = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid qualification name"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Names must be at least 2 characters and have only letters",
            ),
        ]
    )
    fundedfrom = DateField('fundedfrom', format='%d-%m-%Y')
    fundedto = DateField('fundedto', format='%d-%m-%Y')
    typeoffund = SelectField(u'', choices=[('1', 'Bursary'), ('2', 'Loan'), ('3', 'Other')])
    amount = IntegerField(validators=[
            InputRequired(),
            Length(13, message="Please provide a valid amount"),
            Regexp(
                "^R(?!0\d)\d+(?:\.\d{2})?(?=\s|$)",
                0,
                "Amount format R300 or R3000 or R35780. Please round of the amount",
            ),
        ]
    )

class OccupationForm(FlaskForm):
    occupation = StringField(validators=[
            InputRequired(),
            Length(2, 150, message="Please provide a valid occupation"),
            Regexp(
                "^[A-Za-z]{2,25}||\s[A-Za-z]{2,25}",
                0,
                "Occupation must be at least 2 characters and have only letters",
            ),
        ]
    )
    functionalunit = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    employmentstatus = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    municipaldivision = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    placement = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    gross = IntegerField(validators=[
            InputRequired(),
            Length(13, message="Please provide a valid amount"),
            Regexp(
                "^R(?!0\d)\d+(?:\.\d{2})?(?=\s|$)",
                0,
                "Amount format R300 or R3000 or R35780. Please round of the amount",
            ),
        ]
    )
    postlevel = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])
    dateabsorbed = DateField('fundedfrom', format='%d-%m-%Y')
    dateappointed = DateField('fundedfrom', format='%d-%m-%Y')
    experience = SelectField(validators=[InputRequired(), Length(2,16, message = "Please make a selection")])


class ConstraintsForm(FlaskForm):
    note1 = TextAreaField('', [validators.optional(), validators.length(max=10000)])
    note2 = TextAreaField('', [validators.optional(), validators.length(max=10000)])
    note3 = TextAreaField('', [validators.optional(), validators.length(max=10000)])