from flask import current_app, flash, jsonify, redirect, request, url_for
from flask_restx import Namespace, Resource, marshal
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
import werkzeug
from ..extentions import db
from ..models import User, Course
from ..extentions import api
from flask_restx import fields, reqparse


ns = Namespace(
    name="Student Management", path="/api/students", description="Student Management Api"
)


student_model = api.model(
    "Student",
    {
        "id": fields.Integer(readonly=True, description="User name"),
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.String(),
    },
)
