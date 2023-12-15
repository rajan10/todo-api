from mongoengine import Document, StringField


class User(Document):
    username = StringField(max_length=100, required=True)
    password = StringField(max_length=200, required=True)

    def __str__(self):
        return f"<User> {self.name}>"
