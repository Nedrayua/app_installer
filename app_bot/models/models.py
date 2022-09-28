from mongoengine import connect, Document,IntField, StringField, EmailField, BooleanField

from bot import config as conf
from bot.utils import return_content_args as rca


connect(db=conf.DB_NAME, host=conf.HOST_MONGO, port=conf.DB_PORT)


class User(Document):
    telegram_id = IntField(primary_key=True)
    username = StringField(min_length=2, max_length=256)
    first_name = StringField(min_length=2, max_length=256)
    phone_number = StringField(min_length=9, max_length=13)
    email = EmailField()
    user_city = StringField(min_length=2, max_length=25)
    is_blocked = BooleanField(default=False)

    def formatted_data(self):
        """
        returned data about user
        """
        return f'{rca("Id", self.telegram_id, "Empty")}\n{rca("Nik-name", self.username, "Empty")}\n' \
               f'{rca("Name", self.first_name, "Empty")}\n{rca("Phone", self.phone_number, "Empty")}\n' \
               f'{rca("email", self.email, "Empty")}\n{rca("City", self.user_city, "Empty")}'