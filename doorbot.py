#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import RPi.GPIO as GPIO
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sensors
from time import sleep

# Bot token receieved from BotFather
TOKEN = '710783642:AAF5N4QVb90IyENwZ4hV4cjnN2jjI8_jRw4'

# Luis application setup
LUIS_KEY = ''
ENDPOINT = 'https://westeurope.api.cognitive.microsoft.com/luis/v2.0/apps/c3ecb7e9-9c34-4bba-9fbe-ccdab583141a?verbose=true&timezoneOffset=0&subscription-key=9b6dc17ab7d84af6abafefbd324f579f&q='

# Global parameters

##################################################### Command Handlers ##########################################################


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def lock(update, context):
    # sensors.lock()
    update.message.reply_text('The door is closed!')


def unlock(update, context):
    # sensors.unlock()
    update.message.reply_text('The door is open!')


def take_pic(update, context):
    # pic_path = sensors.take_picture()
    # update.message.sendPhoto(photo=open(pic_path, 'rb'))
    update.message.reply_text('Should I open??')


def limit_access(update, context):
    update.message.reply_text("Ok, only family is allowed. I wonder what you're hiding (-;")


###################################################### Language Understanding ###################################################


# Parse the message and call the right command handler
def hadle_text_message(update, context):
    print(update.message.text)
    intent = get_intent(update.message.text)
    print(intent)
    if (intent == "close"):
        lock(update, context)
    elif (intent == "open"):
        unlock(update, context)
    elif (intent == "limit"):
        limit_access(update, context)
    elif(intent == "picture"):
        take_pic(update, context)
    elif (intent == "limit"):
        limit_access(update, context)
    else:
        update.messae.reply_text("Sorry I didn't understand you")


# Send the receieved message to the LUIS application and get the top scoring intent
def get_intent(message):
    # Set up the request headers
    headers = {
        'Ocp-Apim-Subscription-Key': LUIS_KEY,
    }

    try:
        # Send the request to the Luis application endpoint
        r = requests.get(ENDPOINT + message, headers=headers)

        # Get the top scoring intent from the possible intents list
        print(r.json())
        return r.json()['topScoringIntent']['intent']
    except Exception:
        return None


#################################################################################################################################


def main():
    # Set up the bot updater with the bot Token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Set up a commnad handler for each command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("open", unlock))
    dp.add_handler(CommandHandler("close", lock))
    dp.add_handler(CommandHandler("picture", take_pic))
    dp.add_handler(CommandHandler("limit", limit_access))
    # Set up a message handler for text messages
    dp.add_handler(MessageHandler(Filters.text, hadle_text_message))

    # Start listen for incoming messages
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()