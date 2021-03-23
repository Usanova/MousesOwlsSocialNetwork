from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import repository

def aboutMe(update: Update, context: CallbackContext) -> None:
    userId = update.message.chat_id

    owl = repository.getOwl(userId)
    if(owl != None):
        update.message.reply_text(
            'You are owl!\n'
            'Your userName is {userName}\n'.format(userName = owl.userName) +
            'Your happinessLevel is {happinessLevel}\n'.format(happinessLevel = owl.happinessLevel) +
            'Your satietyLevel is {satietyLevel}'.format(satietyLevel = owl.satietyLevel))
        return

    mouse = repository.getMouse(userId)
    if (mouse != None):
        update.message.reply_text(
            'You are mouse!\n'
            'Your userName is {userName}\n'.format(userName = mouse.userName) +
            ("You are alive" if mouse.isLive else "You are dead"))
        return

    update.message.reply_text(
        'You are not registered!')

def live(update: Update, context: CallbackContext) -> None:
    userId = update.message.chat_id

    mouse = repository.getMouse(userId)

    mouse.isLive = True

    repository.saveMouse(mouse)