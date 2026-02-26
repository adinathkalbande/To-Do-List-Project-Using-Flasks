# from flask import Blueprint, render_template, redirect, request, url_for, flash, session

# auth_bp = Blueprint("auth", __name__)

# USER_CREDENTIALS = {
#     "username": "admin",
#     "password": "12345"
# }

# @auth_bp.route("/login", methods=["GET", "POST"])
# def login():

#     if "user" in session:
#         return redirect(url_for("tasks.view_tasks"))

#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")

#         if username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]:
#             session["user"] = username
#             flash("Login Successful", "success")
#             return redirect(url_for("tasks.view_tasks"))
#         else:
#             flash("Invalid Credential", "danger")

#     return render_template("login.html")


# @auth_bp.route("/logout")
# def logout():
#     session.pop("user", None)
#     flash("Logged Out", "info")
#     return redirect(url_for("auth.login"))





from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if "user" in session:
        return redirect(url_for("tasks.view_tasks"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session["user"] = user.username
            session["user_id"] = user.id

            flash("Login Successful", "success")
            return redirect(url_for("tasks.view_tasks"))

        else:
            flash("Invalid Credential", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged Out", "info")
    return redirect(url_for("auth.login"))