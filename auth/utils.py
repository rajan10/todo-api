import bcrypt
from flask import jsonify, request, make_response
import base64
from user.user_repo import UserRepo

from pydantic import ValidationError


def encrypt_string(string: str):
    bytes = string.encode("utf-8")
    salt = bcrypt.gensalt()
    encrypted_bytes = bcrypt.hashpw(bytes, salt)
    encrypted_string = encrypted_bytes.decode("utf-8")
    return encrypted_string


# encrypt = encrypt_string("abc123")


# db_password = {"password": encrypt}
# db_password = db_password.get("password")
# db_password_bytes = db_password.encode("utf-8")


def compare_password(user_password: str, db_password: str) -> bool:
    user_password_bytes = user_password.encode("utf-8")  # converting both into bytes
    db_password_bytes = db_password.encode("utf-8")

    result = bcrypt.checkpw(user_password_bytes, db_password_bytes)
    return result


# print(compare_password("abc123", db_password_bytes))


def login_required(func):
    def inner_func(*args, **kwargs):
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
                return func(*args, **kwargs)
            else:
                response = make_response(
                    jsonify({"message": "Not Successfully authenticated!"})
                )
                return response
        except ValidationError as exc:
            return make_response(jsonify({"message": exc.errors()}), 400)
        except Exception as exc:
            return make_response(jsonify({"message": str(exc)}), 500)

    return inner_func
