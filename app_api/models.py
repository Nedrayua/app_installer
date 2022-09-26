from mongoengine import connect, Document, IntField, StringField, EmailField, BooleanField
import config as conf

connect(conf.DB_NAME, conf.HOST_MONGO, conf.DB_PORT)


class User(Document):
    telegram_id = IntField(primary_key=True)
    username = StringField(min_length=2, max_length=256)
    first_name = StringField(min_length=2, max_length=256)
    phone_number = StringField(min_length=9, max_length=13)
    email = EmailField()
    user_city = StringField(min_length=2, max_length=25)
    is_blocked = BooleanField(default=False)

    def __repr__(self):
        return f'User username: {self.username}, firstname: {self.first_name}'

