from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import repository

SUBSCRIBEOWLNAME = range(1)

def startSubscribe(update: Update, context: CallbackContext) -> int:
    mouseId = update.message.chat_id

    mouse = repository.getMouse(mouseId)

    if (mouse == None):
        update.message.reply_text(
            'You are not registered as mouse!'
        )
        return ConversationHandler.END

    update.message.reply_text(
        'Enter the name of the owl you want to subscribe to'
    )

    return SUBSCRIBEOWLNAME

def subscribeOwlName(update: Update, context: CallbackContext) -> int:

    owlName = update.message.text

    owl = repository.getOwlByUserName(owlName)
    if (owl == None):
        update.message.reply_text(
            'Owl with `{owlName}` username not registered!'.format(owlName = owlName)
        )
        return ConversationHandler.END

    mouseId = update.message.chat_id
    mouse = repository.getMouse(mouseId)

    owl.registerObserver(mouse)

    repository.saveOwl(owl)

    update.message.reply_text(
        'Greate!'
    )
    return ConversationHandler.END

def cancelSubscribe(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Subscribing canceled!'
    )

    return ConversationHandler.END