import BasicElement as be
import random
from datetime import  datetime

class Owl(be.Subject):
    observers = []
    happinessLevel = 100
    satietyLevel = 0
    lastTimePosting = None

    id = ""
    userName = ""

    def __init__(self, id, userName):
        self.id = id
        self.userName = userName
        self.lastTimePosting = datetime.utcnow()
        self.happinessLevel = 100
        self.satietyLevel = 0
        self.observers = []

    def registerObserver(self, object):
        if object in self.observers:
            return

        self.observers.append(object)

    def removeObserver(self, object):
        self.observers.remove(object)

    def notifyObserver(self, post):
        notifier = be.Notifier()
        notifier = be.EmailNotifier(notifier)
        notifier = be.WhatsAppNotifier(notifier)
        notifier = be.TelegramNotifier(notifier)

        for mouse in self.observers:
            if not mouse.isLive:
                continue

            notifier.send(post, mouse)
            post.addReceiver(mouse)

    def uh(self, post):
        self.notifyObserver(post)
        self.lastTimePosting = datetime.utcnow()

    def eatMouse(self, mouse):
        mouse.dead()
        self.satietyLevel += 1

    def punishForNonPosting(self):
        if(self.happinessLevel < 10):
            self.happinessLevel = 0
        else:
            self.happinessLevel -= 10


class Mouse(be.Object):
    subject = None
    isLive = True

    id = ""
    userName = ""

    def __init__(self, id, userName):
        self.id = id
        self.userName = userName

    def update(self, post):
        if random.random() >= 0.5 :
            post.like(self)

    def dead(self):
        self.isLive = False

    def isDead(self):
        return not(self.isLive)






