from datetime import datetime

from db import User, DoesNotExist

MESSAGES = {
    'morning': 'Доброе утро',
    'day': 'Добрый день',
    'night': 'Добрый вечер'
}


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
    try:
        user = User.objects(telegram_id=message.from_user.id).get()
        greeting_message += ', ' + user.enter_name
        return greeting_message
    except DoesNotExist:
        return greeting_message


def update_or_save_user(message):
    if message.reply_to_message:
        if message.reply_to_message.text == 'Введите свое имя:':
            try:
                user = User.objects(telegram_id=message.from_user.id).get()
                user.update(enter_name=message.text)
                greeting_message = 'Имя было изменено'
            except DoesNotExist:
                user = User(name_from_telegram=message.from_user.username, telegram_id=message.from_user.id, enter_name=message.text)
                user.save()
                greeting_message = 'Ваше имя было сохранено'
            return greeting_message
