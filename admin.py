from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView

from app import app


class UserAdminView(ModelView):
    form_columns = ('enter_name', 'name_from_telegram')
    column_list = ('enter_name', 'name_from_telegram', 'telegram_id')
    can_create = False


admin = Admin(app, 'Telegram names', '/')







