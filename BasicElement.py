from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import abc
from datetime import  datetime
import random
from telegram.ext import Updater
import configparser
config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")

class Post:
    id = 0
    postInformation = "No Information"
    sender = None
    sentTime = None
    likedObjects = []
    receivers = []

    def __init__(self, sender, postInformation):
        self.id = random.randint(0, 10000000)
        self.sender = sender
        self.postInformation = postInformation
        self.sentTime = datetime.utcnow()
        self.likedObjects = []
        self.receivers = []

    def addReceiver(self, object):
        if any(map(lambda receiver: receiver.id == object.id, self.receivers)):
            return

        self.receivers.append(object)

    def like(self, object):
        if any(map(lambda receiver: receiver.id == object.id, self.likedObjects)):
            return

        self.likedObjects.append(object)

    def didLike(self, receiverId):
        return any(map(lambda receiver: receiver.id == receiverId, self.likedObjects))

class Object(abc.ABC):
    @abc.abstractmethod
    def update(self, post):
        pass

class Subject(abc.ABC):
    @abc.abstractmethod
    def registerObserver(self, object):
        pass

    @abc.abstractmethod
    def removeObserver(self, object):
        pass

    @abc.abstractmethod
    def notifyObserver(self, notifier, post):
        pass

class Notifier():
    def send(self, post, receiver):
        print("Notifire observer")

class BaseNotifierDecorator(Notifier):
    notifier = None

    def __init__(self, notifier):
        self.notifier = notifier

    def send(self, post, receiver):
        self.notifier.send(post, receiver)

class EmailNotifier(BaseNotifierDecorator):
    def __init__(self, notifier):
        super(EmailNotifier, self).__init__(notifier)

    def send(self, post, receiver):
        super(EmailNotifier, self).send(post, receiver)
        print("Send to Email")

class WhatsAppNotifier(BaseNotifierDecorator):
    def __init__(self, notifier):
        super(WhatsAppNotifier, self).__init__(notifier)

    def send(self, post, receiver):
        super(WhatsAppNotifier, self).send(post, receiver)
        print("Send to WhatsApp")

LIKEBUTTON = "likeButton"

class TelegramNotifier(BaseNotifierDecorator):

    def __init__(self, notifier):
        super(TelegramNotifier, self).__init__(notifier)


    def send(self, post, receiver):
        super(TelegramNotifier, self).send(post, receiver)

        updater = Updater(config["Bot"]["token"])
        likeButton = InlineKeyboardButton('Like', callback_data='{likeButton}{postId}'.format(likeButton = LIKEBUTTON,
                                                                                            postId = post.id))
        likeMarkup = InlineKeyboardMarkup([[likeButton]])

        updater.bot.send_message(chat_id = receiver.id, text =
        'It`s post from `{owlName}`\n'.format(owlName=post.sender.userName) +
        post.postInformation,
        reply_markup=likeMarkup)
        print("Send to Telegram")

