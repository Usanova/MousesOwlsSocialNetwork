import random
import BasicElement as be
import GameObjects as go
from pymongo import  *

client = MongoClient('localhost', 27017)

db = client['MousesOwls']

posts = []

def saveOwl(owl: go.Owl):
    owlsCollection = db['owls']

    observersId = list(map(lambda observer: observer.id, owl.observers))

    owlData = {
        "id": owl.id,
        "userName": owl.userName,
        "satietyLevel": owl.satietyLevel,
        "lastTimePosting": owl.lastTimePosting,
        "happinessLevel": owl.happinessLevel,
        "observersId": list(map(lambda observer: observer.id, owl.observers))
    }

    if owlsCollection.find_one({'id': owl.id}) == None:
        owlsCollection.insert_one(owlData)
    else:
        owlsCollection.update_one({'id': owl.id}, {'$set': owlData})

    for mouse in owl.observers:
        saveMouse(mouse)


def getOwl(id) -> go.Owl:
    owlsCollection = db['owls']
    owlDate = owlsCollection.find_one({'id': id})

    if owlDate == None:
        return None
    else:
        return createOwlObjectFromData(owlDate)

def getOwlByUserName(userName) -> go.Owl:
    owlsCollection = db['owls']
    owlDate = owlsCollection.find_one({'userName': userName})

    if owlDate == None:
        return None
    else:
        return createOwlObjectFromData(owlDate)

def saveMouse(mouse: go.Mouse):
    mousesCollection = db['mouses']

    mouseData = {
        "id": mouse.id,
        "userName": mouse.userName,
        "isLive": mouse.isLive
    }

    if mousesCollection.find_one({'id': mouse.id}) == None :
        mousesCollection.insert_one(mouseData)
    else :
        mousesCollection.update_one({'id': mouse.id}, {'$set': mouseData})

def getMouse(id) -> go.Mouse:
    mousesCollection = db['mouses']
    mouseDate = mousesCollection.find_one({'id': id})

    if mouseDate == None:
        return None
    else:
        return createMouseObjectFromData(mouseDate)

def savePost(post: be.Post):
    postsCollection = db["posts"]

    postData = {
        "id": post.id,
        "postInformation": post.postInformation,
        "senderId": post.sender.id,
        "sentTime": post.sentTime,
        "receiversId": list(map(lambda receiver: receiver.id, post.receivers)),
        "likeObjectsId": list(map(lambda likedObject: likedObject.id, post.likedObjects))
    }

    if postsCollection.find_one({'id': post.id}) == None:
        postsCollection.insert_one(postData)
    else:
        postsCollection.update_one({'id': post.id}, {'$set': postData})

    saveOwl(post.sender)

    for mouse in post.receivers:
        saveMouse(mouse)

    for mouse in post.likedObjects:
        saveMouse(mouse)

def getPost(id)-> be.Post:
    postCollection = db['posts']
    postDate = postCollection.find_one({'id': id})

    if postDate == None:
        return None
    else:
        return createPostObjectFromData(postDate)

# def register(id, userName):
#     if random.random() >= 0.5 :
#         registerOwl(id, userName)
#     else:
#         registerMouse(id, userName)
f = False

def register(id, userName):
    global f
    if f == True:
        owl = go.Owl(id, userName)
        saveOwl(owl)
    else:
        mouse = go.Mouse(id, userName)
        saveMouse(mouse)
        f = True


def createMouseObjectFromData(mouseData) -> go.Mouse:
    mouse = go.Mouse(mouseData["id"], mouseData["userName"])
    mouse.isLive = bool(mouseData["isLive"])
    return mouse

def createOwlObjectFromData(owlData) -> go.Owl:
    owl = go.Owl(owlData["id"], owlData["userName"])
    owl.lastTimePosting = owlData["lastTimePosting"]
    owl.satietyLevel = owlData["satietyLevel"]
    owl.happinessLevel = owlData["happinessLevel"]

    observersId = list(owlData["observersId"])

    for observerId in observersId:
        owl.registerObserver(getMouse(observerId))

    return owl


def createPostObjectFromData(postData) -> be.Post:
    sender = getOwl(postData["senderId"])

    post = be.Post(sender, postData["postInformation"])
    post.id = postData["id"]
    post.sentTime = postData["sentTime"]

    receiversId = list(postData["receiversId"])

    for receiverId in receiversId:
        post.addReceiver(getMouse(receiverId))

    likeObjectsId = list(postData["likeObjectsId"])

    for likeObjectId in likeObjectsId:
        post.like(getMouse(likeObjectId))

    return post