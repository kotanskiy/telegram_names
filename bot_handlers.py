from bot_utils import *
from bot import bot


@bot.message_handler(commands=['start'])
def start(message):
    greeting_message = add_name_to_greeting_message(message, generate_greeting_message())
    send_rename_button(message, greeting_message)
    bot.send_message(message.chat.id, 'Введите свое имя:')
    bot.register_next_step_handler(message, rename_user)


@bot.message_handler(func=lambda message: message.text == 'Изменить Имя ☝️')
def enter_user_name(message):
    greeting_message = add_name_to_greeting_message(message, generate_greeting_message())
    send_rename_button(message, greeting_message)
    bot.send_message(message.chat.id, 'Введите свое имя:')
    bot.register_next_step_handler(message, rename_user)


# @bot.message_handler(func=is_enter_name_message)
# def rename_user_handler(message):
#     greeting_message = rename_user(message)
#     if not greeting_message:
#         greeting_message = generate_greeting_message()
#     greeting_message = add_name_to_greeting_message(message, greeting_message)
#     send_rename_button(message, greeting_message)


@bot.message_handler(content_types=['text'])
def hello(message):
    greeting_message = add_name_to_greeting_message(message, generate_greeting_message())
    bot.send_message(message.chat.id, greeting_message)



