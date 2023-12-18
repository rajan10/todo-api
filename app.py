from flask import Flask, jsonify, Response
from user.urls import user_blueprint
from task.urls import task_blueprint
from auth.urls import auth_blueprint
from database import db
import json


app = Flask(__name__)  # object creation
app.register_blueprint(user_blueprint)
app.register_blueprint(task_blueprint)
app.register_blueprint(auth_blueprint)

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
    response = Response(
        response=json.dumps({"message": "Server is running"}), status=200
    )
    return response
