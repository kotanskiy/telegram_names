from datetime import datetime

import telebot
from flask import request
from mongoengine import DoesNotExist
from telebot.types import ForceReply, ReplyKeyboardMarkup, KeyboardButton

from app import app
from bot import bot
from config import Config
from db import User


MESSAGES = {
    'morning': 'Доброе утро',
    'day': 'Добрый день',
    'night': 'Добрый вечер'
}


@bot.message_handler(commands=['start'])
def start(message):
    markup = ForceReply(selective=False)
    now = datetime.now().hour
    if 10 > now > 5:
        greeting_message = MESSAGES['morning']
    elif 10 <= now < 18:
        greeting_message = MESSAGES['day']
    else:
        greeting_message = MESSAGES['night']
    bot.send_message(message.chat.id, greeting_message)
    bot.send_message(message.chat.id, 'Введите свое имя:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Изменить Имя ☝️')
def rename_user(message):
    markup = ForceReply(selective=False)
    now = datetime.now().hour
    if 10 > now > 5:
        greeting_message = MESSAGES['morning']
    elif 10 <= now < 18:
        greeting_message = MESSAGES['day']
    else:
        greeting_message = MESSAGES['night']
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('Изменить Имя ☝️')
    keyboard.add(button)
    bot.send_message(message.chat.id, reply_markup=keyboard, text=greeting_message)
    bot.send_message(message.chat.id, 'Введите свое имя:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def hello(message):
    now = datetime.now().hour
    if 10 > now > 5:
        greeting_message = MESSAGES['morning']
    elif 10 <= now < 18:
        greeting_message = MESSAGES['day']
    else:
        greeting_message = MESSAGES['night']
    if message.reply_to_message:
        if message.reply_to_message.text == 'Введите свое имя:':
            try:
                user = User.objects(name_from_telegram=message.chat.username).get()
                user.update(enter_name=message.text)
                greeting_message = 'Имя было изменено'
            except DoesNotExist:
                user = User(name_from_telegram=message.chat.username, telegram_id=message.chat.id, enter_name=message.text)
                user.save()
                greeting_message = 'Ваше имя было сохранено'
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('Изменить Имя ☝️')
    keyboard.add(button)
    bot.send_message(message.chat.id, reply_markup=keyboard, text=greeting_message)


@app.route('/' + Config.TELEGRAM_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/web_hook")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url='https://lit-eyrie-94912.herokuapp.com/web_hook/' + Config.TELEGRAM_TOKEN)
    return "!", 200


# if __name__ == '__main__':
#     bot.polling(none_stop=True)

