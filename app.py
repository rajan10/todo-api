from flask import Flask, request, jsonify
from database import db
from repository import TaskRepo


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
