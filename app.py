from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/")
def hell_world():
    response = {"message": "todo-api is running"}
    return jsonify(response)


@app.route("/hello/<username>")  # path parameter
def hello(username):
    response = {"message": f"Hello {username}"}
    return jsonify(response)


@app.route("/user", methods=["POST"])
def register():
    data = request.json  # dictionary
    print(type(data))
    print(data)
    response = {"message": "Successfully registered"}
    return jsonify(response)


# query parameter task


@app.route("/user")
def query_example():
    name = request.args.get("name")
    age = request.args.get("age")

    response = f"Hello {name}!"
    if age is not None:
        response = response + f" You are  {age} years old!"
    return response
