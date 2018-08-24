import flask


from config import Config


app = flask.Flask(__name__)

app.config.from_object(Config)

from db import User
from admin import admin, UserAdminView

admin.add_view(UserAdminView(User))

from handlers import *
