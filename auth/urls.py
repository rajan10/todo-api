from flask import Blueprint, request, jsonify, make_response
from user.user_repo import UserRepo
from pydantic import ValidationError

from auth.utils import compare_password, login_required, create_access_token
import base64


auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/auth", methods=["POST"])
def user_auth():
    try:
        auth_header = request.headers.get("Authorization")
        encoded_credential = auth_header.split(" ")[1]
        decoded_credential = base64.b64decode(encoded_credential).decode("utf-8")
        username, password = decoded_credential.split(":")
        if not username or not password:
            return make_response(
                jsonify({"message": "No Username or Password provided"}), 400
            )
        user_repo = UserRepo()
        user = user_repo.read_by_username(username=username)
        if not user:
            return make_response(jsonify({"message": "No user"}), 401)
        result = compare_password(user_password=password, db_password=user.password)
        if result:
            response = make_response(
                jsonify({"message": "Successfully authenticated!"})
            )
            return response
        else:
            response = make_response(
                jsonify({"message": "Not Successfully authenticated!"})
            )
            return response
    except ValidationError as exc:
        return make_response(jsonify({"message": exc.errors()}), 400)
    except Exception as exc:
        return make_response(jsonify({"message": str(exc)}), 500)


@auth_blueprint.route("/hello-world", methods=["GET"])
@login_required  # decorator
def hello_world():  # decorated function
    return make_response(jsonify({"message": "Hello world!"}), 200)


@auth_blueprint.route("/login", methods=["POST"])
@login_required
def login():
    access_token = create_access_token(payload={"name": "Hari"})
    return make_response(
        jsonify(
            {"message": "Successfully Authenticated", "access_token": access_token}
        ),
        200,
    )


# get_all_user end point
