from bot_utils import *
from bot import bot


@bot.message_handler(commands=['start'])
def start(message):
    greeting_message = add_name_to_greeting_message(message, generate_greeting_message())
    send_rename_button(message, greeting_message)
    bot.send_message(message.chat.id, 'Введите свое имя:')
    save_next_step_handler(message, rename_user)


@bot.message_handler(func=lambda message: message.text == 'Изменить Имя ☝️')
def enter_user_name(message):
    greeting_message = add_name_to_greeting_message(message, generate_greeting_message())
    bot.send_message(message.chat.id, greeting_message)
    bot.send_message(message.chat.id, 'Введите свое имя:')
    save_next_step_handler(message, rename_user)


@bot.message_handler(content_types=['text'])
def hello(message):
    user = User.objects(telegram_id=message.from_user.id).first()
    if user and user.next_step_func_name:
        globals()[user.next_step_func_name](message)
        user.update(next_step_func_name='')
        return
    greeting_message = add_name_to_greeting_message(message, generate_greeting_message())
    bot.send_message(message.chat.id, greeting_message)



