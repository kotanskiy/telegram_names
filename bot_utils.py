from datetime import datetime
import re

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ForceReply

from bot import bot
from database import User

MESSAGES = {
    'morning': 'Доброе утро',
    'day': 'Добрый день',
    'night': 'Добрый вечер'
}


def is_enter_name_message(message):
    if message.reply_to_message:
        if message.reply_to_message.text == 'Введите свое имя:':
            return True
    return False


def is_valid_name(name):
    pattern = r'[a-zA-Z]{2,20}|[а-яА-Я]{2,20}'
    return True if re.fullmatch(pattern, name) else False


def generate_greeting_message():
    now = datetime.now().hour
    if 10 > now > 5:
        greeting_message = MESSAGES['morning']
    elif 10 <= now < 18:
        greeting_message = MESSAGES['day']
    else:
        greeting_message = MESSAGES['night']
    return greeting_message


def add_name_to_greeting_message(message, greeting_message):
    user = User.objects(telegram_id=message.from_user.id).first()
    if user:
        greeting_message += ', ' + user.enter_name
    return greeting_message


def rename_user(message):
    if not is_valid_name(message.text):
        bot.send_message(message.chat.id, 'Имя не валидно')
        save_next_step_handler(message, rename_user)
        return
    user = User.objects(telegram_id=message.from_user.id).first()
    user.update(enter_name=message.text)
    answer = 'Имя было изменено'
    user.update(next_step_func_name='')
    bot.send_message(message.chat.id, answer)


def send_rename_button(message, greeting_message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
    button = KeyboardButton('Изменить Имя ☝️')
    keyboard.add(button)
    bot.send_message(message.chat.id, reply_markup=keyboard, text=greeting_message)


def send_force_enter_name(message):
    markup = ForceReply()
    bot.send_message(message.chat.id, 'Введите свое имя:', reply_markup=markup)


def save_next_step_handler(message, func):
    user = User.objects(telegram_id=message.from_user.id).first()
    if user:
        user.update(next_step_func_name=func.__name__)
    else:
        user = User(telegram_id=message.from_user.id,
                    name_from_telegram=message.from_user.username,
                    next_step_func_name=func.__name__)
        user.save()

