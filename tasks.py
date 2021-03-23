from celery import Celery
import repository
from datetime import *

app = Celery('tasks',
             backend='rpc://',
             broker='pyamqp://guest@localhost//')

@app.task
def checkPost(postId : int):
    print("start")
    post = repository.getPost(postId)

    owl = post.sender

    for mouse in post.receivers:
        if not post.didLike(mouse.id):
            owl.eatMouse(mouse)

    repository.savePost(post)
    return post.id

@app.task
def punishForNonPosting(owlId : int):
    owl = repository.getOwl(owlId)

    if datetime.utcnow() - owl.lastTimePosting > timedelta(seconds=300):
        owl.punishForNonPosting()

    return "punishForNonPosting"

#print("Hi")