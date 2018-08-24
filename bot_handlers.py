from telebot.types import ForceReply, ReplyKeyboardMarkup, KeyboardButton
from bot_utils import *
from bot import bot


@bot.message_handler(commands=['start'])
def start(message):
    markup = ForceReply(selective=False)
    greeting_message = generate_greeting_message()

    try:
        user = User.objects(telegram_id=message.chat.id)
        greeting_message += ', ' + user.enter_name
    except DoesNotExist:
        pass
    bot.send_message(message.chat.id, greeting_message)
    bot.send_message(message.chat.id, 'Введите свое имя:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Изменить Имя ☝️')
def rename_user(message):
    markup = ForceReply(selective=False)
    greeting_message = generate_greeting_message()
    try:
        user = User.objects(telegram_id=message.chat.id)
        greeting_message += ', ' + user.enter_name
    except DoesNotExist:
        pass
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('Изменить Имя ☝️')
    keyboard.add(button)
    bot.send_message(message.chat.id, reply_markup=keyboard, text=greeting_message)
    bot.send_message(message.chat.id, 'Введите свое имя:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def hello(message):
    greeting_message = update_or_save_user(message)
    if not greeting_message:
        greeting_message = generate_greeting_message()
    try:
        user = User.objects(telegram_id=message.chat.id)
        greeting_message += ', ' + user.enter_name
    except DoesNotExist:
        pass
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('Изменить Имя ☝️')
    keyboard.add(button)
    bot.send_message(message.chat.id, reply_markup=keyboard, text=greeting_message)

