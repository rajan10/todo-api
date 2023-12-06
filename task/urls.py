from flask import Blueprint, request, jsonify

from task.task_repo import TaskRepo


task_blueprint = Blueprint("task_blueprint", __name__)


@task_blueprint.route("/task-create", methods=["POST"])
def create():
    data = request.json
    title = data["title"]
    description = data["description"]
    due_date = data["due_date"]

    task_repo = TaskRepo()
    task_repo.create(title=title, description=description, due_date=due_date)
    return jsonify({"message": f"Task {title} created successfully!"})


@task_blueprint.route("/task-read/<title>", methods=["GET"])
def read(title: str):
    task_repo = TaskRepo()
    task = task_repo.read_by_title(title=title)
    return jsonify(task)


@task_blueprint.route("/task-update/<title>", methods=["PUT"])
def update(title: str):
    data = request.json
    description = data.get("description")
    due_date = data.get("due_date")
    is_completed = data.get("is_completed")
    task_repo = TaskRepo()
    task = task_repo.update_by_title(
        title=title,
        description=description,
        due_date=due_date,
        is_completed=is_completed,
    )
    return jsonify(task)


@task_blueprint.route("/task-delete/<title>", methods=["DELETE"])
def delete(title: str):
    task_repo = TaskRepo()
    task_repo.delete(title=title)
    return jsonify({"message": f"Task {title} deleted successfully!"})
