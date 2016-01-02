from app import *
from app.vote.models import *

db.__init__(app)

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
            return 'finish'
            break
        count += 1
