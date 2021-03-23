import random
import BasicElement as be
import GameObjects as go
from telegram import Update
import TelegramBotCommand.registerCommand as rc
import TelegramBotCommand.subscribeCommand as sc
import TelegramBotCommand.postCommand as pc
import TelegramBotCommand.aboutMeCommand as amc
import configparser
config = configparser.ConfigParser()
config.read("settings.ini")

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, \
    CallbackQueryHandler


def main():

    updater = Updater(config["Bot"]["token"])

    dispatcher = updater.dispatcher

    register_handler = ConversationHandler(
        entry_points=[CommandHandler('register', rc.startRegister)],
        states={
            rc.USERNAME: [MessageHandler(Filters.text & ~Filters.command, rc.userName)],
        },
        fallbacks=[CommandHandler('cancelRegister', rc.cancelRegister)],
    )
    dispatcher.add_handler(register_handler)

    subscribe_handler = ConversationHandler(
        entry_points=[CommandHandler('subscribe', sc.startSubscribe)],
        states={
            sc.SUBSCRIBEOWLNAME: [MessageHandler(Filters.text & ~Filters.command, sc.subscribeOwlName)],
        },
        fallbacks=[CommandHandler('cancelPost', sc.cancelSubscribe)],
    )

    dispatcher.add_handler(subscribe_handler)

    post_handler = ConversationHandler(
        entry_points=[CommandHandler('post', pc.startPost)],
        states={
            pc.POSTINFORMATION: [MessageHandler(Filters.text & ~Filters.command, pc.postInformation)],
        },
        fallbacks=[CommandHandler('cancelPost', pc.cancelPost)],
    )

    dispatcher.add_handler(post_handler)

    like_handler = CallbackQueryHandler(
        callback = pc.like
    )
    dispatcher.add_handler(like_handler)

    dispatcher.add_handler(CommandHandler("aboutMe", amc.aboutMe))

    dispatcher.add_handler(CommandHandler("live", amc.live))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

