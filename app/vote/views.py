from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.core.db import db
from .forms import InputID
from .models import User, Question, User_answer

vote_views = Blueprint('vote', __name__, template_folder='../templates', static_folder='../static')

#Index route
@vote_views.route('/', methods=['GET', 'POST'])
def inputID():
    if 'user_id' in session:
        return redirect(url_for('.question'))
    form = InputID()
    #handle POST method
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(form.full_name.data, form.email.data, form.birthday.data)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('.question'))
        form.email.errors.append("Email has been registered")
    #handle GET method
    return render_template('inputID.html', form=form)


#vote route
@vote_views.route('/question/', methods=['POST', 'GET'])
def question():
    #check session
    if "user_id" not in session:
        flash("You're not registered, Enter your date if you wanto register")
        return redirect(url_for('.inputID'))

    ####Handle question view####
    for x in Question.query.all():
        if not User_answer.query.filter_by(user_id=session['user_id'], question_id=x.id).first():
            question = Question.query.get(x.id)
            break
    else:
        return redirect(url_for('.thanks'))

    #handle post method
    if request.method == "POST":
        if request.form["answer"] == "YES": answer = 1
        else: answer = 0
        db.session.add(User_answer(session["user_id"], question.id, answer))
        db.session.commit()
        return redirect(url_for('.question'))

    ### HANDLE GET METHOD ###
    return render_template('question.html', question=question)

@vote_views.route('/thanks/')
def thanks():
    #check session
    if 'user_id' in session:
        #check count the number of questions answered
        if Question.query.count() is not User_answer.query.filter_by(user_id=session['user_id']).count():
            flash("You must answer all question!")
            return redirect(url_for('.question'))
        #remove all session
        session.clear()
    else:
        flash("You must register to Answer question")
        return redirect(url_for('.inputID'))
    return render_template('thanks.html')
