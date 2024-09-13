#!/usr/bin/env python3
""" basic flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"])
def pay_load():
    """ return """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """ registers
    new user
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email and password:
            try:
                user = AUTH.register_user(email, password)
            except ValueError:
                return jsonify({"message": "email already registered"}), 400
        return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def log_in():
    """logs in
    a user
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        has_logged = AUTH.valid_login(email, password)
        if not has_logged:
            abort(401)
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def log_out():
    """ logs the user
    out of the application
    """
    id_session = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(id_session)
    if user:
        destroy_session(user.id)
        return redirect(url_for('/'))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """ check if user session
    still exist"""
    id_session = request.cookies.get("session_id")
    if not id_session:
        abort(403)
    user = AUTH.get_user_from_session_id(id_session)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """reset user password"""
    email = request.form["email"]
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email,
                       "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ update password """
    email = request.form["email"]
    token = request.form["reset_token"]
    password = request.form["new_password"]
    try:
        AUTH.update_password(token, password)
        return jsonify({"email": email,
                       "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port="5000")
