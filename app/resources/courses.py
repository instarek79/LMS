from flask import current_app, flash, jsonify, redirect, request, url_for
from flask_restx import Namespace, Resource, marshal, marshal_with
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
import werkzeug
from ..extentions import db
from ..models import Topic, User, Course, Student, CourseStudentAssociation
from ..extentions import api
from flask_restx import fields, reqparse
from ..resources.student import student_model
from .topic import topic_model
ns = Namespace(
    name="Courses Management", path="/api/courses", description="Course Management Api"
)


course_model = api.model(
    "Course",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(),
        "description": fields.String(),
        "image": fields.String(),
        "topics": fields.List(fields.Nested(topic_model)),
        "students": fields.List(fields.Nested(student_model)),
        "quizzes": fields.List(fields.String),
    },
)


@ns.route("/get_managed_course")
class get_managed_course(Resource):
    def get(self):
        if not current_user.is_authenticated and not current_user.role == "professor":
            return {"message": "Unauthorized"}, 401
        return marshal(current_user.managed_courses, course_model)


# @ns.route("/add")
# class create_new_course(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument("name", required=True, location="form")
#     parser.add_argument("description", required=True, location="form")
#     parser.add_argument(
#         "image",
#         type=werkzeug.datastructures.FileStorage,
#         location="files",
#         required=True,
#     )

#     @ns.expect(parser, validate=True)
#     def post(self):
#         if not current_user.is_authenticated and not current_user.role == "professor":
#             return {"message": "Unauthorized"}, 401
#         args = self.parser.parse_args()
#         try:
#             img = args["image"]
#             name = secure_filename(img.filename)
#             img.save(f"app/static/courseimages/{name}")
#             new_course = Course(
#                 name=args["name"],
#                 description=args["description"],
#                 image=f"/static/courseimages/{name}",
#                 professor_id=current_user.id,
#             )

#             db.session.add(new_course)
#             db.session.commit()
#             flash("Course Added", "success")
#             return {"message": "Course Added"}, 201
#         except:
#             db.session.rollback()
#             flash("Error Adding Course", "danger")
#             return {"message": "Error Adding Course"}, 500


@ns.route("/get_students/<int:id>")
class get_course_students(Resource):
    @marshal_with(student_model)
    @ns.response(401, "Unauthorized")
    @ns.response(404, "Course Not Found")
    @ns.response(200, "Course Found", model=student_model)
    def get(self, id):
        if not current_user.is_authenticated:
            return {"message": "Unauthorized"}, 401

        course = Course.query.filter_by(id=id).first_or_404()

        return course.students


@ns.route("/get_students_not/<int:id>")
class get_course_students_not(Resource):
    @marshal_with(student_model)
    @ns.response(401, "Unauthorized")
    @ns.response(404, "Course Not Found")
    @ns.response(200, "Course Found", model=student_model)
    def get(self, id):
        if not current_user.is_authenticated:
            return {"message": "Unauthorized"}, 401

        course = Course.query.filter_by(id=id).first_or_404()
        all_students = Student.query.all()
        students_not = [
            student for student in all_students if student not in course.students
        ]
        return students_not


course_student = api.model(
    "CourseStudent",
    {
        "course_id": fields.Integer(required=True),
        "student_id": fields.Integer(required=True),
    },
)


@ns.route("/add_student_to_course")
@ns.route("/remove_student_from_course")
class remove_student_from_course(Resource):

    def delete(self):
        if current_user.is_anonymous or not current_user.role == "professor":
            return {"message": "Unauthorized"}, 401
        args = ns.payload
        course = Course.query.get_or_404(args["course_id"])
        student = Student.query.get_or_404(args["student_id"])
        
        try:
            course.students.remove(student)
            db.session.commit()
            flash("student removed from course", "success")
            return {"message": "student removed from course"}, 200
        except:
            db.session.rollback()
            flash("Error Removing Student", "danger")
            return {"message": "Error Removing Student"}, 500


@ns.route("/add_students")
class add_student_to_course(Resource):

    def put(self):
        """Add Student to course"""
        if current_user.is_anonymous or not current_user.role == "professor":
            return {"message": "Unauthorized"}, 401
        args = ns.payload
        print(args)
        students = []
        for entry in args:
            if entry["name"] == "students":
                students.append(entry.get("value"))
            elif entry["name"] == "course_id":
                course = Course.query.get_or_404(entry.get("value"))

        try:
            for student in students:
                course.students.append(Student.query.get_or_404(student))

            db.session.commit()
            flash("students added to course", "success")
            return {"message": "student added to course"}, 200
        except:
            db.session.rollback()
            flash("Error Adding Student", "danger")
            return {"message": "Error Adding Student"}, 500


@ns.route("/get_topics/<int:course_id>")
class get_topics(Resource):
    @ns.response(401, "Unauthorized")
    @ns.response(404, "Course Not Found")
    @ns.response(
        200,
        "Course Found",
        model=topic_model,
    )
    @ns.marshal_list_with(topic_model, skip_none=True, mask=None)
    def get(self, course_id):
        if current_user.is_anonymous or not current_user.role == "professor":
            return {"message": "Unauthorized"}, 401
        course = Course.query.get_or_404(course_id)

        return course.topics


@ns.route("/add_topic/<int:course_id>")
class add_topic(Resource):
    @ns.response(401, "Unauthorized")
    @ns.response(404, "Course Not Found")
    @ns.response(
        200,
        "Topic Added",
        model=topic_model,
    )
    @ns.expect(topic_model,validate=True)
    def post(self, course_id):
        if current_user.is_anonymous or not current_user.role == "professor":
            return {"message": "Unauthorized"}, 401
        course = Course.query.get_or_404(course_id)
        if current_user != course.professor:
            return {"message": "Unauthorized"}, 401
        # Topic
        print(ns.payload)
        topic = Topic(
            name=ns.payload["name"],
            content=ns.payload["content"],
            course_id=course_id
        )
        try:
            db.session.add(topic)
            db.session.commit()
        except:
            db.session.rollback()
            flash("Error Adding Topic", "danger")
            return {"message": "Error Adding Topic"}, 500
        flash("Topic Added", "success")
        return {'message': 'Topic Added'} , 200


@ns.route('/remove_topic_from_course')
class remove_topic(Resource):
    parsereq=reqparse.RequestParser()
    parsereq.add_argument('topic_id',type=int,required=True)
    parsereq.add_argument('course_id',type=int,required=True)
    @ns.expect(parsereq,validate=True)
    def delete(self):
        topic=Topic.query.get_or_404(ns.payload['topic_id'])
        course=Course.query.get_or_404(ns.payload['course_id'])
        if topic in course.topics:
            try:
                db.session.delete(topic)
                db.session.commit()
                flash('Successfully removed topic','success')
                return {'message':'Successfully removed topic'},200
            except:
                db.session.rollback()
                flash('Error Removing Topic','danger')
                return {'message':'Error removing topic'},500
            

@ns.route('/delete/<int:id>')
class delete_course(Resource):
    def delete(self, id):
        course = Course.query.get_or_404(id)
        if current_user.role == "professor" and current_user != course.professor:
            return {"message": "Unauthorized"}, 401
        try:
            db.session.delete(course)
            db.session.commit()
            flash('Course Deleted','success')
            return {"message": "Course Deleted"}, 200
        except:
            db.session.rollback()
            return {"message": "Error Deleting Course"}, 500    