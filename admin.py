from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView

from app import app


class UserAdminView(ModelView):
    form_columns = ('enter_name', 'name_from_telegram')
    can_create = False


admin = Admin(app, 'Telegram names', '/')







