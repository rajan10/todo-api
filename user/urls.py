from flask import Blueprint, request, jsonify
from user.user_repo import UserRepo

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/user-create", methods=["POST"])
def create_user():
    data = request.json
    username = data["username"]
    password = data["password"]

    user_repo = UserRepo()
    user = user_repo.create(username=username, password=password)
    return jsonify(user)


@user_blueprint.route("/user-read/<username>", methods=["GET"])
def read_user(username: str):
    user_repo = UserRepo()
    user = user_repo.read_by_username(username=username)
    return jsonify(user)


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
