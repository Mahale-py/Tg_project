from peewee import (SqliteDatabase,
                    Model,
                    IntegerField,
                    CharField)


db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    exchange = CharField()
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)


def create_tables():
    db.create_tables(BaseModel.__subclasses__())