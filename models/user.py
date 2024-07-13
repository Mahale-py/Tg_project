from peewee import (SqliteDatabase,
                    Model,
                    IntegerField,
                    CharField)


db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    exchange = CharField(null=True)
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)