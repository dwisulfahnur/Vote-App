from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from app.core.db import db
from .forms import InputID
from .models import User, Question, User_answer

vote_views = Blueprint('vote', __name__, template_folder='../templates', static_folder='../static')

#Index route
@vote_views.route('/', methods=['GET', 'POST'])
def inputID():
    if 'user_id' in session:
        return redirect(url_for('.question', id=1))
    form = InputID()
    #handle POST method
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(form.full_name.data, form.email.data, form.birthday.data)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('.question', id=1))
        form.email.errors.append("Email has been registered")
    #handle GET method
    return render_template('inputID.html', form=form)

def next_post(id):
    count = Question.query.count()
    while (count > 0):
        next_post = None
        id += 1
        if Question.query.get(id) is not None:
            next_post = Question.query.get(id)
            return next_post.id
            break
        if id > count:
            return 0
        count += 1

#vote route
@vote_views.route('/question/<int:id>/', methods=['POST', 'GET'])
def question(id):
    #check session
    if "user_id" not in session:
        flash("You're not registered")
        return redirect(url_for('.inputID'))

    #definition question and user answer content
    question_all = Question.query.all()
    question = Question.query.get(id)
    user_answer = User_answer.query.filter_by(user_id=session['user_id']).all()

    #handle post method
    if request.method == "POST":
        if request.form["answer"] == "YES": answer = 1
        else: answer = 0
        db.session.add(User_answer(session["user_id"], question.id, answer))
        db.session.commit()
        return redirect(url_for('.question', id=next_post(id)))
    if id == 0:
        return redirect(url_for('.thanks'))
    #handle if id question not in DATABASE
    if not question:
        flash("Question ID is not in database")
        return redirect(url_for('.question', id=1))
    #handle repeat answer
    for a in user_answer:
        if question.id == a.question_id:
            return redirect(url_for('.question', id=next_post(question.id)))
    #handle get method
    return render_template('question.html', question=question)

@vote_views.route('/thanks/')
def thanks():
    #check session
    if 'user_id' in session:
        #check count the number of questions answered
        if Question.query.count() is not User_answer.query.filter_by(user_id=session['user_id']).count():
            flash("You must answer all question!")
            return redirect(url_for('.question', id=1))
        #remove all session
        session.clear()
    else:
        flash("You must register to Answer question")
        return redirect(url_for('.inputID'))
    return render_template('thanks.html')
