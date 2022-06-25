from flask import Blueprint, flash, render_template, request, redirect, url_for, Flask, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required

# project file imports
from website.forms import UserLoginForm, ObjectUploadForm, UserSignupForm
from website.models import User, Post, db, check_password_hash, post_schema, posts_schema

#from file upload tutorial for images and files
import os
from werkzeug.utils import secure_filename
from config import Config

auth = Blueprint('auth', __name__, template_folder ='auth_templates')

#----------------------SIGN_UP--------------------------
@auth.route('/signup', methods = ['GET','POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            # Add User into Database
            test = User.query.filter(User.email == email).first()
            if email == test:
                print(email, 'already in db')
                flash(f'{email} already has an account with us.','auth-failed')
                return redirect(url_for('auth.login'))
            else:
                user = User(email,password = password)
                db.session.add(user)
                db.session.commit()
                flash(f'You have successfully created a user account for {email}.', "user-created")
                
                #login new user & redirect to inventory page
                logged_user = User.query.filter(User.email == email).first()
                login_user(logged_user)
                
                return redirect(url_for('site.profile'))
    except:
        raise Exception('Invalid Form Data: Please check your form.')

    return render_template('signup.html', form=form)

#----------------------LOG_IN--------------------------
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            #---------Query user table for users with this info----------------
            logged_user = User.query.filter(User.email == email).first()

            #----------Check if logged_user and password == password--------------
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your Email/Password is incorrect.', 'auth-failed')
                return redirect(url_for('auth.login'))

    except:
        raise Exception('Invalid Form Data: Please check your form.')

    return render_template('login.html', form=form)

#----------------------UPLOAD_FORM--------------------------
@auth.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload():
    form = ObjectUploadForm()
    try:
        if request.method == 'POST':
            title = form.title.data
            description = form.description.data
            price = form.price.data
            dimensions = form.dimensions.data
            weight = form.weight.data
            img_url = upload_image()
            model_url = upload_model()
            user_token = current_user.token
            print(title, description, price, dimensions, weight, img_url, model_url)

            post = Post(title, description, price, dimensions, weight, img_url, model_url, user_token)

            db.session.add(post)
            db.session.commit()

            flash('Model Successfully Uploaded!', 'mode-made')
            return redirect(url_for('site.inventory'))
    except:
        raise Exception('Something went wrong')

    return render_template('upload.html', form=form)


#-----------------------UPLOAD_IMAGE-------------------------
# def allowed_file(filename):
#     return '.' in filename and \
        #    filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'obj', 'stl'} #Config.ALLOWED_EXTENSIONS

#@app.route("/upload", methods=['GET', 'POST'])
def upload_image():
    #if request.method == 'POST':

    #check to see if file exists
    if request.files:  
        file = request.files["image"]

    # print(Config.UPLOAD_FOLDER)
    # print(file)
    #check for allowed file type, and upload the file
    #if file and allowed_file(file.filename):
    #filename = secure_filename(file.filename)
    file.save(os.path.join(Config.UPLOAD_FOLDER, file.filename))
    return '../../static/uploads/' + file.filename  #directory file path (static) + file name

#-----------------------UPLOAD_MODEL-------------------------
def upload_model():
    if request.files:  
        file = request.files["model"]

    file.save(os.path.join(Config.UPLOAD_FOLDER, file.filename))
    print(file.filename)
    return '../../static/uploads/' + file.filename 
#-----------------------UPDATE_POST-------------------------

# def update_image():
#     if request.files:  
#         file = request.files["image"]
#     file.save(os.path.join(Config.UPLOAD_FOLDER, file.filename))
#     return '../../static/uploads/' + file.filename

# def update_model():
#     if request.files:  
#         file = request.files["model"]
#     file.save(os.path.join(Config.UPLOAD_FOLDER, file.filename))
#     return '../../static/uploads/' + file.filename 

@auth.route('/update/<id>', methods = ['GET', 'POST', 'PUT'])
@login_required
def update_post(id):
    form = ObjectUploadForm()
    post_update = Post.query.get(id)

    if request.method == 'POST':
        post_update.title = request.form['title']
        post_update.description = request.form['description']
        post_update.dimensions = request.form['dimensions']
        post_update.weight = request.form['weight']
        # post_update.img_url = request.form[update_image()]
        # post_update.title = request.form[update_model()]
        post_update.id = id
        post_update.user_token = post_update.user_token
        try:
            db.session.commit()
            post_schema.dump(post_update)
            flash("Update Successful!")
            render_template('update.html', form=form, post_update = post_update)
            return redirect(url_for('site.inventory'))
        except:
            # flash("Update Error, try again!")
            return render_template('update.html', form=form, post_update = post_update)
    else:
        return render_template('update.html', form=form, post_update = post_update)

#--------------------------DOWNLOAD----------------------
@auth.route('/', methods = ['GET', 'POST'])  #url path doesn't seem to affect anything, investigate this
#/static/uploads/
# @login_required
def download():
    # try:
    return send_from_directory(Post.model_url)
        # os.path.join(Config.UPLOAD_FOLDER, file.filename), filename=model_url, as_attachment=True )

    # except FileNotFoundError:
    #     abort(404)

#------------------------DELETE------------------------

@auth.route('/delete/<id>', methods = ['GET'])
@login_required
def delete_post(id):
    #id passed in from JinJa
    post = Post.query.get(id)  #gets the db row via id
    # post = Post.query.get_or_404(id)  #tutorial code, this works too
    db.session.delete(post)
    db.session.commit()
    post_schema.dump(post)

    return redirect(url_for('site.inventory'))

#-------------------------BUY-----------------------

@auth.route('/inventory', methods = ['GET','POST'])  #de-bug this
def seller_email():
    flash(f'Purchase feature comming soon!!')
    # return redirect(url_for('site.inventory'))

#----------------------LOGOUT--------------------------

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))

