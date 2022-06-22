"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Placeholder kitten photos
default_image_url = "http://placekitten.com/g/500/500"

class User(db.Model):
    """User"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.String, nullable=False, default=default_image_url)

    def __repr__(self):
        """Show info about user object"""
        u = self
        return f"<User name is {u.get_full_name} and id is {u.id}>"

    @property
    def get_full_name(self):
        """give users full name"""
        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

