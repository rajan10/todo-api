from flask import Blueprint, request, jsonify, make_response
from user.user_repo import UserRepo
from user.schemas import UserBaseSchema, UserNameSchema, UserDeleteSchema, UserSchema
from pydantic import ValidationError
from auth.utils import encrypt_string


user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/user-create", methods=["POST"])
def create_user():
    try:
        data = request.json
        # validation and unpackaging of data dict
        user_create_schema = UserBaseSchema(**data)
        username = user_create_schema.username
        password = user_create_schema.password
        encrypted_password = encrypt_string(string=password)
        user_repo = UserRepo()
        user = user_repo.create(username=username, password=encrypted_password)
        user_schema = UserSchema(
            id=user.id, username=user.username, password=user.password
        )
        response = make_response(jsonify(user_schema.model_dump()), 201)

        return response

    except ValidationError as exc:
        return make_response(
            jsonify({"message": exc.errors()}),
            400,
        )
    except Exception as exc:
        return (
            make_response(jsonify({"message": str(exc)})),
            500,
        )


@user_blueprint.route("/user-read/<username>", methods=["GET"])
def read_user(username: str):
    try:
        user_read_schema = UserNameSchema(username=username)
        user_repo = UserRepo()
        user = user_repo.read_by_username(username=user_read_schema.username)
        user_schema = UserSchema(
            id=user.id, username=user.username, password=user.password
        )
        response = make_response(jsonify(user_schema.model_dump()), 200)
        return response
    except ValidationError as exc:
        return make_response(jsonify({"message": exc.errors()}), 400)
    except Exception as exc:
        return make_response(jsonify({"message": str(exc)}), 500)


@user_blueprint.route("/user-update/<username>", methods=["PUT"])
def update_user(username: str):
    try:
        data = request.json
        user_update_schema = UserBaseSchema(**data)
        password = user_update_schema.password
        user_repo = UserRepo()
        user = user_repo.update_by_username(
            username=user_update_schema.username, password=password
        )
        user_schema = UserSchema(
            id=user.id, username=user.username, password=user.password
        )
        response = make_response(jsonify(user_schema.model_dump()), 201)
        return response
    except ValidationError as exc:
        return make_response(jsonify({"message": exc.errors()}), 400)
    except Exception as exc:
        return make_response(jsonify({"message": str(exc)}), 500)


@user_blueprint.route("/user-delete/<username>", methods=["DELETE"])
def delete_user(username: str):
    try:
        username_delete_schema = UserDeleteSchema(username=username)
        user_repo = UserRepo()
        user_repo.delete_by_username(username=username_delete_schema.username)
        response = make_response(
            jsonify({"message": f"Successfully deleted!{username}"}), 204
        )
        return response
    except ValidationError as exc:
        return make_response(jsonify({"message": exc.errors()}), 400)
    except Exception as exc:
        return make_response(jsonify({"message": str(exc)}), 500)
