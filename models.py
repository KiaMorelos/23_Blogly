"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

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

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user object"""
        u = self
        return f"<User name is {u.get_full_name} and id is {u.id}>"

    @property
    def get_full_name(self):
        """give users full name"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Posts"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """Show info about post object"""
        p = self
        return f"<Post>"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)