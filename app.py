from flask import Flask, jsonify
from user.urls import user_blueprint
from task.urls import task_blueprint
from database import db


app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(task_blueprint)


app.config["MONGODB_SETTINGS"] = [
    {
        "db": "todo-api",
        "host": "localhost",
        "port": 27017,
    }
]
db.init_app(app)


@app.route("/")
def health_status():
    return jsonify({"message": "Server is running"})
