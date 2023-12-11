from flask import Blueprint, request, jsonify
from user.user_repo import UserRepo
from user.schemas import UserCreateSchema, UserReadSchema
from pydantic import ValidationError

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/user-create", methods=["POST"])
def create_user():
    try:
        data = request.json
        # validation and unpackaging of data dict
        user_create_schema = UserCreateSchema(**data)
        username = user_create_schema.username
        password = user_create_schema.password

        user_repo = UserRepo()
        user = user_repo.create(username=username, password=password)
        return jsonify(user)
    except ValidationError as exc:
        return jsonify({"message": exc.errors()})
    except Exception as exc:
        return jsonify({"message": str(exc)})


@user_blueprint.route("/user-read/<username>", methods=["GET"])
def read_user(username: str):
    try:
        user_read_schema = UserReadSchema(username=username)
        user_repo = UserRepo()
        user = user_repo.read_by_username(username=user_read_schema.username)
        return jsonify(user)
    except ValidationError as exc:
        return jsonify({"message": exc.errors()})
    except Exception as exc:
        return jsonify({"message": str(exc)})


@user_blueprint.route("/user-update/<username>", methods=["PUT"])
def update_user(username: str):
    data = request.json
    password = data.get("password")
    user_repo = UserRepo()
    user = user_repo.update_by_username(username=username, password=password)
    return jsonify(user)


@user_blueprint.route("/user-delete/<username>", methods=["DELETE"])
def delete_user(username: str):
    user_repo = UserRepo()
    user_repo.delete_by_username(username=username)
    return jsonify({"message": f"Successfully deleted!{username}"})
