"""Seed file to make sample data for people db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add people
tyler = User(first_name='Tyler',last_name="Hogan")
lydia = User(first_name='Lydia', last_name="Hogan")
hannah = User(first_name='Hannah', last_name="Hogan")

db.session.add(tyler)
db.session.add(lydia)
db.session.add(hannah)

db.session.commit()