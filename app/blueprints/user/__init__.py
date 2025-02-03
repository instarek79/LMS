import re
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user, logout_user
import flask_login
from app.models import Admin, User, Student
from app.wtf_forms import SignupForm
from app.extentions import db, bcrypt

# Create a Blueprint for your routes
login_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

app = login_blueprint


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated != True:
        if request.method == "POST":
            next = request.args.get("next")
            username = request.form.get("username")
            password = request.form.get("password")
            user_object = User.query.filter_by(username=username).first()
            if user_object:
                try:
                    if bcrypt.check_password_hash(user_object.password, password):
                        flask_login.login_user(user_object)
                        if user_object.role=="admin":
                            return redirect(url_for("admin.index"))
                        return redirect(next)
                except Exception as e:
                    flash(f"Username or Password is invalid {e}", "danger")
                    return redirect(url_for(".login", next=next))
            flash("Username or Password is invalid", "danger")

            return redirect(url_for(".login", next=next))
        return render_template("auth/login.html")
    else:
        return redirect(url_for("home.index"))


@app.route("/register", methods=["GET", "POST"])
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    form2 = SignupForm()

    if form2.validate_on_submit():
        next = request.args.get("next")
        user_data = form2.data.copy()
        user_data.pop("confirm")
        user_data.pop("submit")
        user_data.pop("csrf_token")
        # print(user_data["password"])
        # print(user_data["username"])
        # if (
        #     re.match(
        #         r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        #         user_data["password"],
        #     )
        #     is None
        # ):
        #     flash("Invalid Password Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character and at least 8 characters long", "danger")
        #     return render_template("auth/signup.html", form=form2)
        user_data["password"] = bcrypt.generate_password_hash(user_data["password"])
        # if re.match(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$',user_data["username"]) is None:
        #     flash('Invalid Username','danger')
        print([i.username for i in User.query.all()])
        print((user_data["username"] in [i.username for i in User.query.all()]))
        if (user_data["username"] in [i.username for i in User.query.all()]):
            flash("Username Already Exists", "danger")
            return render_template("auth/signup.html", form=form2)
        if user_data["email"] in [i.email for i in User.query.all()]:
            flash("Email Already Exists", "danger")
            return render_template("auth/signup.html", form=form2)
        user = Student(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user)
            flash("User Successfully Created", "success")
            return redirect(url_for("home.index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error In database {e}", "danger")
            return render_template("auth/signup.html", form=form2)
    elif form2.errors:
        flash(form2.errors, "danger")
    return render_template("auth/signup.html", form=form2)


@app.route("/logout")
@login_required
def logout():
    next = request.args.get("next")
    logout_user()
    return redirect(url_for("home.index"))
