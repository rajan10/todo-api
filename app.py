from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/")
def hell_world():
    response = {"message": "todo-api is running"}
    return jsonify(response)  # Converts Python objects -> JSON format


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
# query parameter are seperated by &


@app.route("/user")
def query_example():
    name = request.args.get(
        "name"
    )  # name is queryparameter and Ram as value;query string is name=Ram
    age = request.args.get("age", default="N/A")

    response = f"Hello {name}!"
    if age is not None:
        response = response + f" You are  {age} years old!"
    return response


@app.route("/blog/<int:postID>")
def show_blog(postID):
    return f"Blog Number: {postID}"


@app.route("/api/example", methods=["GET"])
def example():
    data = {"key": "value", "number": 42, "is_enabled": True}
    return jsonify(data)


@app.route("/api/greet", methods=["GET", "POST"])
def greet():
    if request.method == "GET":
        name = request.args.get("name", "Guest")
        age = request.args.get("age", default="N/A")
        return jsonify(
            {
                "message": f"Hello {name}! Welcome to the Flask API. You are {age}years old!"
            }
        )
    elif request.method == "POST":
        data = request.json  #dict
        print(type(data))
        name = data.get("name", "Guest")
        email = data.get("email")
        return jsonify(
            {
                "message": f"Hello, {name}! Your email is {email} Welcome to the Flask API!"
            }
        )
