import bcrypt
from flask import jsonify, request, make_response
import base64
from user.user_repo import UserRepo
from functools import wraps
from pydantic import ValidationError
import jwt
from jwt.exceptions import InvalidTokenError, InvalidSignatureError


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


def login_required(func):  # func =hello_world() or decorated function
    @wraps(func)
    def inner_func(
        *args, **kwargs
    ):  # this is extra or inner function/wrapper function that modifies/decorates
        # decorated hello_world function or in short this wrapper modifies the behavior of decorated fun hello_world
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
                return func(*args, **kwargs)  # call hello_world which is  function
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


def create_access_token(payload: dict) -> str:
    access_token = jwt.encode(payload, "9898", algorithm="HS256")
    return access_token


def authorization_required(func: callable):
    @wraps(func) # is a decorator function that updates the wrapper function to look like the decorated function(func).This is often used 
    # to preserve metadata such as the the function name and docstring
    def wrapper(*args, **kwargs):  # this is the actual decorated function that will  replace the original function when 
        # 'authorization_required' is appled eg hello_world or def login()
        try:   # token extraction and validation
            access_token = request.headers["Authorization"].split(" ")[1] 
            decoded_payload = jwt.decode(access_token, "9898", algorithms=["HS256"])
            if not decoded_payload:
                return make_response(
                    jsonify({"message": "Incorrect access token"}), 400
                )
            return func(*args, **kwargs) # if access token is valid, the original 'func' is called with its arguments and keyword arguments
        except (InvalidTokenError, InvalidSignatureError) as exc:
            return make_response(
                jsonify({"message": f"Invalid token signature {str(exc)}"}), 400
            )
        except Exception as exc:
            return make_response(jsonify({"message": str(exc)}), 500)

    return wrapper

 """The login function is decorated with authorization_required. This means that before login function is executed, the access 
 token in the Authorization header will be checked and validated using the logic defined in the authorization_required decorator.
 
 A JSON Web Token (JWT) is an open, industry-standard RFC 7519 method for representing claims securely between two parties. It is an encoded string consisting of three parts separated by dots (.). The first part contains the header
, the second part contains the payload, and the third part contains the signature.

JWT does authentication and authorization both
 """
