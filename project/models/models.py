from settings.db_config import db
from datetime import datetime



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(20), default='user')
    last_seen = db.Column(db.Date, nullable=False, default=datetime.now().date())
    rented_books = db.relationship('Book', backref=db.backref('user'), lazy=True)


    def __repr__(self):
        return self.username
    

class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=datetime.now().date())
    description = db.Column(db.Text)
    books = db.relationship('Book',  cascade="all, delete-orphan", backref=db.backref('section'), lazy=True)


    def __repr__(self):
        return self.name


# Define Book model
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False, default=datetime.now().date())
    return_date = db.Column(db.DateTime, nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))


    def __repr__(self):
        return self.name
    


class Feedback(db.Model):
    __tablename__ = 'feedback'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), primary_key=True)
    content = db.Column(db.Text, nullable=False)



class RentRequest(db.Model):
    __tablename__ = 'rent_request'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), primary_key=True)