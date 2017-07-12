# -*- coding: utf-8 -*-

#benötigte Pakete: - telegram libraray
#                  - chatterbot library


#libraries importieren
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram.ext
import time,sys,traceback
import time
import logging
import json
import RPi.GPIO as GPIO




#setup des programms
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


#variablen:
#custom kyboard für telegram
global kb_markup


#servos
global servo1
global servo2
global motor1
global motor2
#global chatbot

servo1 = 24
servo2 = 23






           

#message, command und error verarbeitung
def start(bot, update):
    update.message.reply_text('Hi!, wie gehts?')

def help(bot, update):
    update.message.reply_text('Hi,bist du einsam? starte doch eine Konversation mit /start  :D')

def echo(bot, update):
    print('shit')
        

def front(bot, update):
    #vorwärts bewegung der beiden servos
    motor1.ChangeDutyCycle(9)
    motor2.ChangeDutyCycle(5.6)
    
def back(bot, update):
    #rückwärtsbewegung der beiden servos
    motor1.ChangeDutyCycle(5.6)
    motor2.ChangeDutyCycle(9)
    
    
def left(bot, update):
    #linksbewegung
    motor1.ChangeDutyCycle(5.6)
    motor2.ChangeDutyCycle(5.6)
    
    
def right(bot, update):
    #rechtsbewegung
    motor1.ChangeDutyCycle(9)
    motor2.ChangeDutyCycle(9)


def photo(bot, update):

    bot.send_photo(chat_id=update.message.chat_id, photo=open('Pictures/picture.png', 'rb'))
    
def control(bot, update):
    #öffnet über telegramm das custom keyboard zum steuern des bots
    global kb
    global kb_markup
    kb = [[telegram.KeyboardButton('/front')],
          [telegram.KeyboardButton('/left'),"/stop","/right"],
          [telegram.KeyboardButton('/back')],
          [telegram.KeyboardButton('/photo')]]
    kb_markup = telegram.ReplyKeyboardMarkup(kb)
    bot.send_message(chat_id=update.message.chat_id,
                     text="steuerung gestartet",
                     reply_markup=kb_markup)


          


def endcontrol(bot, update):
    #stoppt motoren
    motor1.ChangeDutyCycle(100)
    motor2.ChangeDutyCycle(100)
    

def stopmotors():
    #stoppt motoren
    motor1.ChangeDutyCycle(100)
    motor2.ChangeDutyCycle(100)
    

def neustartbot(bot, update):
    print('shit')


def error():
    print('error')



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
        updater = Updater("378767153:AAEcr5ahO66RMSjhj1EaQTdfCMsDJ77k18A")
        #("378767153:AAEcr5ahO66RMSjhj1EaQTdfCMsDJ77k18A") #TokenDorian
        #("251884323:AAHNXN9M6TF9cjyiVuUtYGpqUrBQWwtdATc") #TokenSebastian

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
        dp.add_handler(CommandHandler("photo", photo))
        dp.add_handler(MessageHandler(Filters.text, echo))
        dp.add_error_handler(error)

        #startet den bot
        updater.start_polling()

        updater.idle()

    


if __name__ == '__main__':
    main()
