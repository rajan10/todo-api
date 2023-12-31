# views
from flask import Blueprint, request, jsonify, make_response
from user.user_repo import UserRepo
from user.schemas import UserBaseSchema, UserNameSchema, UserDeleteSchema, UserSchema
from pydantic import ValidationError
from auth.utils import encrypt_string, authorization_required, APIError
import base64
from auth.utils import compare_password
from functools import wraps


user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/user-create", methods=["POST"])
@authorization_required  # decorator function: intended to be used other function (create_user) and its purpose is to check n validate
# an access token provided in the 'Authorization' header of an HTTP request. If valid then only decorated function gets called, otherwise error
def create_user():  # decorated function
    try:
        data = request.json  # username and password coming from postman/client
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
        raise APIError(message=exc.errors(), status_code=400)


@user_blueprint.route("/user-read/<username>", methods=["GET"])
@authorization_required
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
        raise APIError(message=exc.errors(), status_code=400)


@user_blueprint.route("/user-update/<username>", methods=["PUT"])
@authorization_required
def update_user(username: str):
    try:
        data = request.json  # data is a dict
        user_update_schema = UserBaseSchema(
            **data
        )  # creating an instance from UserBaseSchema and initializing
        # its attributes with values from 'data' dictionary. the **data syntax is used to unpack dict
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
        raise APIError(message=exc.errors(), status_code=400)


@user_blueprint.route("/user-delete/<username>", methods=["DELETE"])
@authorization_required
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
        raise APIError(message=exc.errors(), status_code=400)


@user_blueprint.route("/users", methods=["GET"])
@authorization_required
def read_all():
    try:
        user_repo = UserRepo()
        users = (
            user_repo.read_all()
        )  # list of users from repository and seralize them before sending
        # them as a JSON response. Serialization is the process of converting complex data types such as data structure
        # or objects into a JSON format which can be easily stored, transmitted or reconstructed later.
        serialized_users = []
        for user in users:
            user_schema = UserSchema(  # user_schema is used to create a schema for user, specifying which user attributes
                # to include in the serialization
                id=user.id,
                username=user.username,
                password=user.password,
            )
            serialized_user = (
                user_schema.model_dump()
            )  # convert user_schema into native python dictionary
            serialized_users.append(serialized_user)
        response = make_response(jsonify({"result": serialized_users}), 200)
        return response
    except ValidationError as exc:
        raise APIError(message=exc.errors(), status_code=400)


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
