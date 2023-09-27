from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
from pytz import timezone
from datetime import datetime
import re

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('Etc/GMT-3')))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone('Etc/GMT-3')))

    @validates('name')
    def validate_name(self, key, name):
        assert name is not None, "Author must have a name!"
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        assert len(phone_number) == 10, "Phone number must be at least 10 digits!"
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name}, phone_number={self.phone_number})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('Etc/GMT-3')))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone('Etc/GMT-3')))

    @validates('title')
    def validate_title(self, key, title):
        assert title is not None, "Post must have a title"

        clickbait_phrases = ["Won't Believe", "Secret", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            if not re.search(r'Top \d+', title):
                raise AssertionError("Title must be clickbait-y")
        return title
    
    @validates('content')
    def validate_content(self, key, content):
        assert len(content) >= 250, "Post content must be at least 250 characters!"
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        assert len(summary) <= 250, "Post summary must be a maximum of 250 characters!"
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        assert category in ['Fiction', 'Non-Fiction'], "Post category must be either Fiction or Non-Fiction!"
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
