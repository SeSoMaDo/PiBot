from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from chatterbot import ChatBot
import telegram.ext
import nxt, time,sys,traceback,nxt.locator, nxt.brick
from nxt.motor import *
from nxt.sensor import *
import time
import logging
import json
import RPi.GPIO as GPIO





logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



global kb_markup
global chatbot
global servo1
global servo2
global motor1
global motor2
global chatbot

servo1 = 24
servo2 = 23

chatbot= ChatBot(
    'Tele Rover',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

chatbot.train("chatterbot.corpus.german")






           

#message, command und error verarbeitung
def start(bot, update):
    update.message.reply_text('Hi!, wie gehts?')

def help(bot, update):
    update.message.reply_text('Hi,bist du einsam? starte doch eine Konversation mit /start  :D')

def echo(bot, update):
    #update.message.reply_text(update.message.text)
    try:
        antwort = str(chatbot.get_response(update.message.text))
    except:
        antwort = chatbot.get_response(update.message.text)
    if antwort.find("/") != -1:
        if antwort.find("send_picture") != -1:
            print ("hier würde ich jetzt das Bild schicken")
            #control()
        else:
            print ("ungültige anweisung")
    update.message.reply_text('%s' % antwort)
        

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def front(bot, update):
    motor1.ChangeDutyCycle(9)
    motor2.ChangeDutyCycle(4)
    
def back(bot, update):
    motor1.ChangeDutyCycle(4)
    motor2.ChangeDutyCycle(9)
    
    
def left(bot, update):
    motor1.ChangeDutyCycle(4)
    motor2.ChangeDutyCycle(4)
    
    
def right(bot, update):
    motor1.ChangeDutyCycle(9)
    motor2.ChangeDutyCycle(9)
    
    
def control(bot, update):
    global kb
    global kb_markup
    kb = [[telegram.KeyboardButton('/front')],
          [telegram.KeyboardButton('/left'),"/stop","/right"],
          [telegram.KeyboardButton('/back')]]
    kb_markup = telegram.ReplyKeyboardMarkup(kb)
    bot.send_message(chat_id=update.message.chat_id,
                     text="steuerung gestartet",
                     reply_markup=kb_markup)


          


def endcontrol(bot, update):
    motor1.ChangeDutyCycle(100)
    motor2.ChangeDutyCycle(100)
    

def stopmotors():
    motor1.ChangeDutyCycle(100)
    motor2.ChangeDutyCycle(100)
    

def neustartbot(bot, update):
    chatbot.train("chatterbot.corpus.english")
    chatbot.train("chatterbot.corpus.german")




def main():
    global motor1
    global motor2
    while True:
        #erstellen der servos
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(servo1, GPIO.OUT)
        GPIO.setup(servo2, GPIO.OUT)
        motor1 = GPIO.PWM(servo1, 50)
        motor2 = GPIO.PWM(servo2, 50)
        #starten der pwm signale
        motor1.start(2.5)
        motor2.start(2.5)
        #stand by der motoren einstellen
        stopmotors()

        
        #erstellt handler
        updater = Updater("251884323:AAHNXN9M6TF9cjyiVuUtYGpqUrBQWwtdATc")

        #registriert sich
        dp = updater.dispatcher
    
        #erstellen der command... listener
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("front", front))
        dp.add_handler(CommandHandler("back", back))
        dp.add_handler(CommandHandler("left", left))
        dp.add_handler(CommandHandler("right", right))
        dp.add_handler(CommandHandler("control", control))
        dp.add_handler(CommandHandler("endcontrol", endcontrol))
        dp.add_handler(CommandHandler("stop", endcontrol))
        dp.add_handler(CommandHandler("neustartbot", neustartbot))
        dp.add_handler(MessageHandler(Filters.text, echo))
        dp.add_error_handler(error)

        #startet den bot
        updater.start_polling()

        updater.idle()

    


if __name__ == '__main__':
    main()
        
