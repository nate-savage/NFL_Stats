from flask import Flask, render_template, redirect, session, request
from flask import flash

from flask_app import app
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/login_page')
def login_page():
    session['logged_in'] = False
    user=0
    if 'user_id' in session:
        session['logged_in']=True
        user = User.get_one({'id':session['user_id']})
    return render_template('login.html', logged_in = session['logged_in'], user=user)

#register post route
@app.route('/submit', methods=['POST'])
def make_user():
    #put some validations here
    if not User.register_validator(request.form):
        return redirect('/login_page')
    user_id =User.create(request.form)
    session['user_id']=str(user_id)
    return redirect('/login_page')

#login post route
@app.route('/login', methods=['POST'])
def login():
    #check based on email
        #then check pw hash
    #if no email match 
    user = User.check_email(request.form)
    if not user:
        flash('Invalid email')
        return redirect('/login_page')
    if  not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('bad password')
        return redirect('/login_page')
    session['user_id'] = str(user.id)

    return redirect('/login_page')


#logout
@app.route('/logout')
def logout():
    session.clear()
    session['logged_in']=False
    return redirect('/')
