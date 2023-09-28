from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Note, Personal, Upload
from . import db
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from .forms import EditProfileForm, PersonalForm, FundingForm
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



views = Blueprint('views', __name__)
""" views.config['MAX_CONTENT_LENGTH'] = 10240 * 1024
views.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.pdf', '.doc', '.docx']
views.config['UPLOAD_PATH'] = 'uploads' """



@views.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

""" @views.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=current_user) """

@views.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    """ posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ] """
    return render_template('user.html', user=current_user)


@views.route('/edit_profile/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)



@views.route('/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def home():
    form = PersonalForm()
    if form.validate_on_submit():
        """ title = [{'titl': 'Ms'}, {'titl': 'Miss'}, {'titl': 'Mrs'}, {'titl': 'Mr'}, {'titl': 'Rev'}, {'titl': 'Dr'}, {'titl': 'Prof'}] """
        title = request.form.get('title')
        flash('title added!', category='success')
        name = request.form.get('name')
        surname = request.form.get('surname')
        idtype = request.form.get('idtype')
        idno = request.form.get('idno')
        passportno = request.form.get('passportno')
        nationality = request.form.get('nationality')
        disability = request.form.get('disability')
        race = request.form.get('race')
        employeeno = request.form.get('employeeno')
        jobtitle = request.form.get('jobtitle')
        phoneno= form.phoneno.data
        department = request.form.get('department')
        municipality = request.form.get('municipality')
        license = request.form.get('license')

        
        newpersonal = Personal(
                        title = title,
                        name = name,
                        surname = surname,
                        idtype = idtype,
                        idno = idno,
                        passportno = passportno,
                        nationality = nationality,
                        disability = disability,
                        race = race,
                        employeeno = employeeno,
                        jobtitle = jobtitle,
                        phoneno = phoneno,
                        department = department,
                        municipality = municipality,
                        license = license,
                    )
                        
        db.session.add(newpersonal) #adding the info to the database 
        db.session.commit()
        flash('Personal info added!', category='success')
       
    return render_template("home.html", user=current_user, form=form)

@views.route('/showphone')
def show_phone():
    return render_template('show_phone.html', phoneno=session['phoneno'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'doc', 'docx', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@views.errorhandler(413)
def too_large(e):
    return make_response(jsonify(message="File is too large"), 413)

@views.route('/qualifications/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def qualifications():
     """ if request.method == 'POST':
        #file = request.files['file']
        file = request.files.get("file")
        print(request.files.get('file'))
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f'Uploaded: {file.filename}'
 """
     if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', "danger")
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file', "danger")
            return redirect(request.url)
        if file and not allowed_file(file.filename):
            return 'File type not allowed', 400
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            upload = Upload(filename=secure_filename(file.filename), data=file.read())
            db.session.add(upload)
            db.session.commit()
            flash('File successfully uploaded', "success")
            return f'Uploaded: {file.filename}'
            #return redirect(url_for('uploaded_file', filename=filename))
    
     return render_template("qualifications.html", user=current_user)

@views.route('/qualdetails/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def qualdetails():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("qualdetails.html", user=current_user)


@views.route('/funding/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def funding():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """ 

    return render_template("funding.html", user=current_user)


@views.route('/occupation/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def occupation():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("occupation.html", user=current_user)

@views.route('/constraints/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def constraints():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("constraints.html", user=current_user)

@views.route('/membership/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def membership():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("membership.html", user=current_user)

@views.route('/competencies/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def competencies():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("competencies.html", user=current_user)


@views.route('/development/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def development():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("development.html", user=current_user)


@views.route('/nationalkpis/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def nationalkpis():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("nationalkpis.html", user=current_user)


@views.route('/rpl/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def rpl():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("rpl.html", user=current_user)


@views.route('/experience/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def experience():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("experience.html", user=current_user)

# create download function for download files
@views.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True)



@views.route('/delete-note/', methods=['POST'], strict_slashes=False)
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/knowledge/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def knowledge():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("knowledge.html", user=current_user)


@views.route('/training/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def training():
    """ if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """

    return render_template("training.html", user=current_user)

""" note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success') """


""" def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@views.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@views.route('/qualifications', strict_slashes=False)
def qualifications():
    files = os.listdir(views.config['UPLOAD_PATH'])
    return render_template('qualifications.html', files=files)

@views.route('/qualifications', methods=['POST'], strict_slashes=False)
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in views.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        uploaded_file.save(os.path.join(views.config['UPLOAD_PATH'], filename))
    return '', 204

@views.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(views.config['UPLOAD_PATH'], filename) """""" form = FundingForm()
    if form.validate_on_submit():
            fundedqual = form.fundedqual.data
            fundedfrom = form.fundedfrom.data
            fundedto = form.fundedto.data
            typeoffund = form.typeoffund.data
            amount = form.amount.data
             """
            
""" fundeduser = FundedUser(
                fundedqual = fundedqual,
                fundedfrom = fundedfrom,
            fundedto = fundedto,
            typeoffund = typeoffund,
            amount = amount,
            )
    
            db.session.add(fundeduser)
            db.session.commit()
            login_user(fundeduser, remember=True)
            flash(f"Fundeduser Succesfully created", "success")
            return redirect(url_for("auth.login"))   """    




