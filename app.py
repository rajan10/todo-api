from flask import Flask
from database import db

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "todo-api",
        "host": "localhost",
        "port": 27017,
    }
]
db.init_app(app)
