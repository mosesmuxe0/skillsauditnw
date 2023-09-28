from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from os import path
from flask_login import LoginManager

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from .models import User, Note, Personal

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath



login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "info"



db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()
bcrypt = Bcrypt()


""" db = SQLAlchemy() """

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

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


class Knowledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timemanagement = db.Column(db.String(80), nullable=False)
    peoplemanagement = db.Column(db.String(80), nullable=False)
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
    comliteracy = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    def __init__(self, timemanagement, peoplemanagement, interpersonal, planning, financial, communication, reportwriting, projmanagement, leadership, diversity, eq, conflict, comliteracy):
        self.timemanagement = timemanagement
        self.peoplemanagement = peoplemanagement
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
        self.comliteracy = comliteracy


""" class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') """


class User(UserMixin, db.Model):
    """ __tablename__ = "User" """
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my beautiful wife'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB_NAME'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

    """ app.config['MAX_CONTENT_LENGTH'] = 10240 * 1024
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.pdf', '.doc', '.docx']
    app.config['UPLOAD_PATH'] = join(dirname(realpath(__file__)), 'static/uploads/..') """
   

    """ def validate_image(stream):
        header = stream.read(512)
        stream.seek(0)
        format = imghdr.what(None, header)
        if not format:
            return None
        return '.' + (format if format != 'jpeg' else 'jpg')

    @app.errorhandler(413)
    def too_large(e):
        return "File is too large", 413

    @app.route('/qualifications', strict_slashes=False)
    def qualifications():
        files = os.listdir(app.config['UPLOAD_PATH'])
        return render_template('qualifications.html', files=files)

    @app.route('/qualifications', methods=['POST'], strict_slashes=False)
    def upload_files():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
                return "Invalid image", 400
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return '', 204

    @app.route('/uploads/<filename>')
    def upload(filename):
        return send_from_directory(app.config['UPLOAD_PATH'], filename) """

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    #db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Personal

    
    
    
    with app.app_context():
        db.create_all()
        

    #login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
