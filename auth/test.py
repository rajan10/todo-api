import bcrypt
from flask import make_response, jsonify, Blueprint, request
from user.user_repo import UserRepo
from pydantic import ValidationError

from utils import compare_password

auth_blueprint = Blueprint("auth_blueprint", __name__)


def login_required(func):
    def inner_func(*args, **kwargs):
        try:
            auth_header = request.headers.get("Authorization")
            encoded_credential = auth_header.split(" ")[1]
            decoded_credential = encoded_credential.decode("utf-8")
            username, password = decoded_credential.split(":")
            if not username or not password:
                return make_response(jsonify({"message": "No User"}), 401)
            user_repo = UserRepo()
            user = user_repo.read_by_username(username=username)
            if not user:
                return make_response(jsonify({"message": "No user"}), 401)
            result = compare_password(user_password=password, db_password=user.password)
            if result:
                return inner_func(*args, **kwargs)
            else:
                response = make_response(
                    jsonify({"message": "Not successfully authenticated"})
                )
                return response
        except ValidationError as exc:
            return make_response(jsonify({"messaage": exc.errors()}))
        except Exception as exc:
            return make_response({"message": exc.errors()}, 400)


# in auth/urls.py
@auth_blueprint.route("/update", methods=["GET"])
@login_required
def update():
    return make_response(jsonify({"message": "Record updated Successfully"}), 200)
