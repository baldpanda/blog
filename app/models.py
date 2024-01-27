from datetime import datetime
from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Further fields like password, profile picture, etc.


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posts = db.relationship("Post", backref="category", lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", name="fk_category_table_id"),
        nullable=True,
    )
