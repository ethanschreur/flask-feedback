from models import User, db, Feedback
from app import app
from flask_bcrypt import Bcrypt

db.drop_all()
db.create_all()

bcrypt = Bcrypt()
hashed = bcrypt.generate_password_hash("Ebobbers@99")
hashed_utf8 = hashed.decode("utf8")

ethan = User(username = "ethanschreur", password = hashed_utf8, email="ethanschreur@icloud.com", first_name="Ethan", last_name="Schreur")
db.session.add(ethan)
db.session.commit()

feedback = Feedback(title = "Awesome Job", content="I loved the presentation. 100 out of 100.", username = ethan.username)

db.session.add(feedback)
db.session.commit()