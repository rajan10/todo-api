from flask import Blueprint, request, jsonify, make_response
from user.user_repo import UserRepo

from auth.utils import compare_password
import base64


auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/auth", methods=["POST"]) 
def user_auth():
    auth_header = request.headers.get("Authorization")
    encoded_credential = auth_header.split(" ")[1]
    decoded_credential = base64.b64decode(encoded_credential).decode("utf-8")
    username, password = decoded_credential.split(":")
    user_repo = UserRepo()
    user = user_repo.read_by_username(username=username)
    if user:
        result = compare_password(user_password=password, db_password=user.password)
    if result == True:
        response = make_response(jsonify({"message": "Successfully authenticated!"}))
        return response

    response = make_response(jsonify({"message": "Not Successfully authenticated!"}))
    return response
