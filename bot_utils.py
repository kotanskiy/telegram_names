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


def update_or_save_user(message):
    if message.reply_to_message:
        if message.reply_to_message.text == 'Введите свое имя:':
            try:
                user = User.objects(telegram_id=message.chat.id).get()
                user.update(enter_name=message.text)
                greeting_message = 'Имя было изменено'
            except DoesNotExist:
                user = User(name_from_telegram=message.chat.username, telegram_id=message.chat.id, enter_name=message.text)
                user.save()
                greeting_message = 'Ваше имя было сохранено'
            return greeting_message
