from flask import Flask, render_template, session, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterUserForm, LoginUserForm, FeedbackForm
from models import User, db, connect_db, Feedback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback-db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shhhh'

connect_db(app)

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        try:
            user = User.register(username = username, password=password, email=email, first_name=first_name, last_name=last_name)
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
            return redirect(f'/users/{user.username}')  
        except:
            form.username.errors = ['Username might be used already']
            form.email.errors =['Or Email might be used already']
            return render_template('register.html', form=form)      
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username = username, password = password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Incorrect Username or Password']
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def username(username):
    if "username" not in session or session["username"] != username:
        return redirect('/login')
    user = User.query.filter_by(username = username).first()
    feedback = user.feedback
    return render_template("username.html", user=user, feedback=feedback)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop("username")
    return redirect("/")

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if "username" not in session or session['username'] != username:
        return redirect('/login')
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        try:
            feedback = Feedback(title = title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        except: 
            return render_template('add_feedback.html', form=form)
    return render_template('add_feedback.html', form=form)

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    if "username" not in session or session['username'] != feedback.username:
        return redirect('/login')
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    return render_template('update_feedback.html', form=form)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_username(username):
    user = User.query.filter_by(username = username).first()
    if "username" in session and session["username"] == username:
        db.session.delete(user)
        db.session.commit()
        session.pop("username")
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        return redirect('/login')
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{feedback.username}')