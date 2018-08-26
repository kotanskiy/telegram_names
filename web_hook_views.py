import telebot
from flask import request

from app import app
from bot import bot
from config import Config


@app.route('/web_hook/' + Config.TELEGRAM_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/web_hook")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url='https://lit-eyrie-94912.herokuapp.com/web_hook/' + Config.TELEGRAM_TOKEN)
    return "!", 200


@app.route('/remove_web_hook')
def remove_web_hook():
    bot.remove_webhook()
    return "!", 200
