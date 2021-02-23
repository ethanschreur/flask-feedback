from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.Text, unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, unique = True, nullable = False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)

    feedback = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, db.ForeignKey("users.username"), nullable=False)