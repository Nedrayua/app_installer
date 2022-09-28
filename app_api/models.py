from mongoengine import connect, Document, IntField, StringField, EmailField, BooleanField
import config as conf

connect(db=conf.DB_NAME, host=conf.HOST_MONGO, port=conf.DB_PORT)


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

