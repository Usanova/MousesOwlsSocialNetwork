from telegram import Update, bot, CallbackQuery
from telegram.ext import CallbackContext, ConversationHandler
import repository
import BasicElement as be
from tasks import checkPost, punishForNonPosting
from datetime import  *
import configparser
config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")

POSTINFORMATION = range(1)


def startPost(update: Update, context: CallbackContext) -> int:

    owlId = update.message.chat_id

    owl = repository.getOwl(owlId)

    if(owl == None):
        update.message.reply_text(
            'You are not registered as owl!'
        )
        return ConversationHandler.END

    update.message.reply_text(
        'Enter the post Information'
    )

    return POSTINFORMATION

def postInformation(update: Update, context: CallbackContext) -> int:
    owlId = update.message.chat_id

    owl = repository.getOwl(owlId)

    postInformation = update.message.text

    post = be.Post(owl, postInformation)

    owl.uh(post)

    update.message.reply_text(
        'Great!'
    )

    repository.savePost(post)
    check = config["WaitingTime"]["checkPostPeriod"]
    checkPost.apply_async(args=[post.id], countdown=int(config["WaitingTime"]["checkPostPeriod"]))
    #punishForNonPosting.apply_async(args=[owl.id], countdown=int(config["WaitingTime"]["punishForNonPosting"]))
    #r = checkPost.apply_async(args=[post.id], countdown=5)
    #result = r.get()
    #print(result)

    return ConversationHandler.END


def cancelPost(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Posting canceled!'
    )

    return ConversationHandler.END

def like(update: Update, callback_query: CallbackQuery):
    if(not(update.callback_query.data.startswith(be.LIKEBUTTON))):
        return

    mouseId = update.callback_query.message.chat_id

    mouse = repository.getMouse(mouseId)

    postId = int(update.callback_query.data[len(be.LIKEBUTTON):])

    post = repository.getPost(postId)

    post.like(mouse)

    repository.savePost(post)




