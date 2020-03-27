#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import re

import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from constants import Const
from load_config import config
from twitter_utils import get_user_timeline

# Enable logging
from word_cloud import word_cloud_generator

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SERVICES, SCREEN_NAME, LOCATION, BIO = range(4)


def start(update: Update, context):
    reply_keyboard = [[Const.cloud_words]]
    user = update.effective_user
    logger.info("start name= %s", user.full_name)

    update.message.reply_text(
        'سلام {name} عزیز☺️\n'
        '🌹 به ربات توییت گرام خوش اومدی 🌹\n'
        'یکی از گزینه های زیر رو انتخاب کن.'
        '👇🏻👇🏻👇🏻👇🏻👇🏻'.format(name=user.first_name),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SERVICES


def get_screen_name(update, context):
    logger.info("cloud_word")
    update.message.reply_text('نام کاربری (username) حساب توییتری مورد نظرتو برام بنویس.',
                              reply_markup=ReplyKeyboardRemove())

    return SCREEN_NAME


def word_cloud(update: Update, context):
    screen_name = update.message.text
    chat_id = update.effective_message.chat_id
    context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
    statuses = get_user_timeline(screen_name)
    tweets = [status.full_text for status in statuses]
    tweet_str = ' '.join(tweets)
    tweet_str = tweet_str.replace("RT", "")
    tweet_str = tweet_str.replace("https", "")
    tweet_str = tweet_str.replace("@", "")
    tweet_str = tweet_str.replace("CO", "")
    tweet_str = tweet_str.replace(screen_name, "")
    tweet_str = re.sub(r'[a-zA-Z]+', '', tweet_str)
    context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
    image_binary = word_cloud_generator(tweet_str)
    caption = 'ابر کلمات توییت های کاربر 👈🏻 {screen_name}\n' \
              'توسط توییتگرام 🤖 @teletweet_bot'.format(screen_name=screen_name)
    update.message.reply_photo(photo=image_binary, caption=caption)
    return ConversationHandler.END


def skip_photo(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config['bot']['token'], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SERVICES: [MessageHandler(Filters.regex('^(' + Const.cloud_words + ')$'), get_screen_name)],

            SCREEN_NAME: [MessageHandler(Filters.text, word_cloud)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
