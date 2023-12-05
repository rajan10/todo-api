from flask import Flask, request, jsonify
from database import db
from repository import TaskRepo, UserRepo


app = Flask(__name__)
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


@app.route("/task-create", methods=["POST"])  # to add
def create():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")

    task_repo = TaskRepo()
    task = task_repo.create(title=title, description=description, due_date=due_date)
    return jsonify(task)


@app.route("/task-read/<title>", methods=["GET"])  # to fetch/ retrieve
def read(title: str):
    task_repo = TaskRepo()
    task = task_repo.read_by_title(title=title)
    if task:
        return jsonify(task)


@app.route("/task-update/<title>", methods=["PUT"])  # title is called as path parameter
def update(title: str):
    task_repo = TaskRepo()

    data = request.json
    description = data.get("description")
    due_date = data.get("due_date")
    is_completed = data.get("is_completed")

    task = task_repo.update_by_title(
        title=title,
        description=description,
        due_date=due_date,
        is_completed=is_completed,
    )
    return jsonify(task)


@app.route("/task-delete/<title>", methods=["DELETE"])
def delete(title: str):
    task_repo = TaskRepo()

    task_repo.delete(title=title)
    return jsonify({"message": "Task deleted successfully!"})


@app.route("/user-create", methods=["POST"])
def create_user():
    data = request.json
    username = data["username"]
    password = data["password"]

    user_repo = UserRepo()
    user = user_repo.create(username=username, password=password)
    return jsonify(user)


@app.route("/user-read/<username>", methods=["GET"])
def read_user(username: str):
    user_repo = UserRepo()
    user = user_repo.read_by_username(username=username)
    return jsonify(user)


@app.route("/user-update/<username>", methods=["PUT"])
def update_user(username: str):
    data = request.json
    password = data.get("password")
    user_repo = UserRepo()
    user = user_repo.update_by_username(username=username, password=password)
    return jsonify(user)


@app.route("/user-delete/<username>", methods=["DELETE"])
def delete_user(username: str):
    user_repo = UserRepo()
    user_repo.delete_by_username(username=username)
    return jsonify({"message": f"Successfully deleted!{username}"})
