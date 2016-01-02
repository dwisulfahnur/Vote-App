from datetime import datetime
from app.core.db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(25))
    email = db.Column(db.String(30))
    birthday = db.Column(db.DateTime)
    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, full_name, email, birthday):
        self.full_name = full_name
        self.email = email
        self.birthday = birthday

    def __repr__(self):
        return '<User {}>'.format(self.full_name)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    teks = db.Column(db.String(120))

    def __init__(self, teks):
        self.teks = teks

class User_answer(db.Model):
    __tablename__ = 'user_answer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('answers', lazy='dynamic'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question',
        backref=db.backref('answers', lazy='dynamic'))
    answer = db.Column(db.Boolean)

    def __init__(self, user_id, question_id, answer):
        self.user_id = user_id
        self.question_id = question_id
        self.answer = answer

    def __repr__(self):
        return '<UserAnswer %d>'%(self.answer)
