from flask import Blueprint, request, jsonify, make_response
from user.user_repo import UserRepo
from pydantic import ValidationError

from auth.utils import compare_password
import base64


auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/auth", methods=["POST"])
def user_auth():
    try:
        auth_header = request.headers.get("Authorization")
    except Exception as exc:
        return make_response(jsonify({"message": exc.errors()}))
        encoded_credential = auth_header.split(" ")[1]
        decoded_credential = base64.b64decode(encoded_credential).decode("utf-8")
        username, password = decoded_credential.split(":")
        user_repo = UserRepo()
        user = user_repo.read_by_username(username=username)
        if not user:
            raise ValueError("No User!")
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

    return jsonify({"error": "Unexpected error occurred"}), 500
