from flask import Blueprint, request, jsonify

from task.task_repo import TaskRepo
from pydantic import ValidationError
from task.schemas import TaskCreateSchema, TaskUpdateSchema, TaskTitleSchema, TaskSchema

task_blueprint = Blueprint("task_blueprint", __name__)


# decorator associating the def create() with /task-create path parameter
@task_blueprint.route("/task-create", methods=["POST"])
def create():
    try:
        data = request.json
        # create an instance of the 'TaskSchema' class by passing data received from a request
        task_create_schema = TaskCreateSchema(**data)  # argument is a kwargs
        title = task_create_schema.title
        description = task_create_schema.description
        due_date = task_create_schema.due_date

        task_repo = TaskRepo()
        task = task_repo.create(title=title, description=description, due_date=due_date)
        task_schema = TaskSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            due_date=task.due_date,
            is_completed=task.is_completed,
        )

        return jsonify(task_schema.model_dump())
    except ValidationError as exc:
        return jsonify({"message": exc.errors()})
    except Exception as exc:
        return jsonify({"message": str(exc)})


@task_blueprint.route("/task-read/<title>", methods=["GET"])
def read(title: str):
    try:
        task_read_schema = TaskTitleSchema(title=title)
        task_repo = TaskRepo()
        task = task_repo.read_by_title(title=task_read_schema.title)
        #  task_dict = task.to_mongo().to_dict()
        task_schema = TaskSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            due_date=task.due_date,
            is_completed=task.is_completed,
        )
        #  task_schema = TaskSchema(**task_dict)
        return jsonify(task_schema.model_dump())
    except ValidationError as exc:
        return jsonify({"message": exc.errors()})

    except Exception as exc:
        return jsonify({"message": str(exc)})


@task_blueprint.route("/task-update/<title>", methods=["PUT"])
def update(title: str):
    try:
        task_title_schema = TaskTitleSchema(title=title)  # record
        data = request.json
        task_update_schema = TaskUpdateSchema(**data)
        title = task_title_schema.title
        description = task_update_schema.description
        due_date = task_update_schema.due_date
        is_completed = task_update_schema.is_completed
        task_repo = TaskRepo()
        task = task_repo.update_by_title(
            title=title,
            description=description,
            due_date=due_date,
            is_completed=is_completed,
        )
        task_schema = TaskSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            due_date=task.due_date,
            is_completed=task.is_completed,
        )
        return jsonify(task_schema.model_dump())
    except ValidationError as exc:
        return jsonify({"message": exc.errors()})
    except Exception as exc:
        return jsonify({"message": str(exc)})


@task_blueprint.route("/task-delete/<title>", methods=["DELETE"])
def delete(title: str):
    try:
        task_delete_schema = TaskTitleSchema(title=title)
        task_repo = TaskRepo()
        task_repo.delete(title=task_delete_schema.title)
        return jsonify({"message": f"Task {title} deleted successfully!"})
    except ValidationError as exc:
        return jsonify({"message": exc.errors()})
    except Exception as exc:
        return jsonify({"message": str(exc)})
