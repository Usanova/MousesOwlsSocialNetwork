from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import repository

USERNAME = range(1)

def startRegister(update: Update, context: CallbackContext) -> int:

    userId = update.message.chat_id

    owl = repository.getOwl(userId)
    if(owl != None):
        update.message.reply_text(
            'You are already registered as owl!'
        )
        return ConversationHandler.END

    mouse = repository.getMouse(userId)
    if (mouse != None):
        update.message.reply_text(
            'You are already registered as mouse!'
        )
        return ConversationHandler.END

    update.message.reply_text(
        'Enter the user Name'
    )

    return USERNAME

def userName(update: Update, context: CallbackContext) -> int:

    userId = update.message.chat_id
    userName = update.message.text

    owl = repository.getOwlByUserName(userName)
    if (owl != None):
        update.message.reply_text(
            'Owl with this user name already registered!'
        )
        return ConversationHandler.END

    repository.register(userId, userName)

    update.message.reply_text(
        'Greate!'
    )
    return ConversationHandler.END

def cancelRegister(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Registering canceled!'
    )