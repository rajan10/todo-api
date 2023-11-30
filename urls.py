from flask import Flask, jsonify, request
from app import app
from repository import TaskRepo


@app.route("/")
def health_status():
    return jsonify({"message": "Server is running"})


@app.route("/task-create", methods=["POST"])
def create():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")

    task_repo = TaskRepo()
    task = task_repo.create(title=title, description=description, due_date=due_date)
    return jsonify(task)
