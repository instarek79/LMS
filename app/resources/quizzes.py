from datetime import datetime, timedelta
import time
from flask import current_app, flash, jsonify, redirect, request, url_for, json
from flask_restx import Namespace, Resource, marshal, marshal_with
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
import werkzeug
from ..extentions import db
from ..models import (
    Question,
    QuizStudentAssociation,
    Topic,
    User,
    Course,
    Quiz,
    Student,
    CourseStudentAssociation,
    QuizQuestionAssosciation,
)
from ..extentions import api
from flask_restx import fields, reqparse
from ..resources.student import student_model

ns = Namespace(
    name="Quiz Management", path="/api/quizzes", description="Quiz Management Api"
)


quiz_model = api.model(
    "Quiz",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(example="quiz1", required=True),
        "author_id": fields.Integer(readonly=True, required=True),
        "marks": fields.Integer(required=True),
        "date": fields.DateTime(),
    },
)

question_model = api.model(
    "Question",
    {
        "id": fields.Integer(readonly=True, description="Question ID"),
        "text": fields.String(description="Question text"),
        "option_1": fields.String(description="Option 1"),
        "option_2": fields.String(description="Option 2"),
        "option_3": fields.String(description="Option 3"),
        "option_4": fields.String(description="Option 4"),
        "correct_option": fields.Integer(description="Correct option number"),
    },
)
quizquestionassosciationmodel = api.model(
    "QuizQuestionAssosciation",
    {
        "marks": fields.Integer(),
        "question": fields.Nested(question_model),
    },
)
QuizQuestionModel = api.model(
    "QuizQuestion",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "marks": fields.Integer(readonly=True),
        "date": fields.DateTime(),
        "questions": fields.List(fields.Nested(quizquestionassosciationmodel)),
    },
)


@ns.route("/current_user")
class quizzess(Resource):
    @ns.response(401, "Unauthorized access! user not logged in")
    @ns.response(200, "success", quiz_model)
    def get(self):
        if current_user.is_anonymous:
            return "Unauthorized access! User not logged in", 401
        if current_user.role == "student":
            return ns.marshal(current_user.taken_quizzes, quiz_model), 200
        elif current_user.role == "professor":
            return ns.marshal(current_user.created_quizzes, quiz_model), 200


@ns.route("/from_course/<int:course_id>")
class quizzess(Resource):
    @ns.response(401, "Unauthorized access! ")
    @ns.marshal_list_with(quiz_model, code=200)
    def get(self, course_id):
        if current_user.is_authenticated and current_user.role != "professor":
            return "Unauthorized access!", 401
        course = Course.query.get_or_404(course_id)
        return course.quizzes, 200


@ns.route("/")
class quizz(Resource):
    reqparser = reqparse.RequestParser()
    reqparser.add_argument("id", type=int, required=True, location="json")

    @ns.expect(reqparser, validate=True)
    def delete(self):
        if current_user.is_authenticated and current_user.role != "professor":
            return "Unauthorized access!", 401
        quiz_id = ns.payload["id"]

        if not quiz_id:
            return {"response": "Quiz ID not provided"}, 400

        # Fetch the quiz by ID
        quiz = Quiz.query.get(quiz_id)

        if not quiz:
            return {"response": "Quiz not found"}, 404

        # Ensure that only the author (or an authorized user) can delete the quiz
        if quiz.author_id != current_user.id:
            flash("Unauthorized action", "danger")
            return {"response": "Unauthorized action"}, 403

        try:
            # Remove all associated questions
            # Assuming there is a relationship defined in Quiz with cascade,
            # otherwise delete questions manually
            for (
                quiz_question
            ) in quiz.questions:  # This depends on your relationships setup
                db.session.delete(quiz_question)

            # Delete the quiz itself
            db.session.delete(quiz)

            # Commit the changes
            db.session.commit()
            flash("Quiz deleted successfully", "success")
            return {"response": "Quiz deleted successfully"}, 200

        except Exception as e:
            print(e)
            db.session.rollback()
            flash("An error occurred while deleting the quiz", "danger")
            return {"response": "Error occurred while deleting the quiz"}, 500

    def post(self):
        if current_user.is_authenticated and current_user.role != "professor":
            return "Unauthorized access!", 401
        if datetime.strptime(request.form.get("quiztime"), "%Y-%m-%dT%H:%M") - datetime.now() < timedelta(days=2):
            flash("Quiz time cannot be less than 2 days from now", "danger")
            return "Quiz time cannot be less than 2 days from now", 400
        quiz = Quiz(
            name=request.form.get("name"),
            date=datetime.strptime(request.form.get("quiztime"), "%Y-%m-%dT%H:%M"),
            marks=0,
            author_id=current_user.id,
        )
        try:
            db.session.add(quiz)
            # db.session.commit()
            course = Course.query.get_or_404(request.form.get("course_id"))
            course.quizzes.append(quiz)
            # db.session.commit()
            texts = request.form.getlist("text")
            questions_1 = request.form.getlist("option_1")
            questions_2 = request.form.getlist("option_2")
            questions_3 = request.form.getlist("option_3")
            questions_4 = request.form.getlist("option_4")
            marks = request.form.getlist("mark")
            question_count = len(texts)
            total_marks = 0
            for i in range(question_count):
                question = Question(
                    text=texts[i],
                    option_1=questions_1[i],
                    option_2=questions_2[i],
                    option_3=questions_3[i],
                    option_4=questions_4[i],
                    correct_option=request.form.get(f"correct_option_{i+1}"),
                    author_id=current_user.id,
                )
                db.session.add(question)
                # quiz.questions.append(question)
                quiz_question = QuizQuestionAssosciation(
                    question=question, quiz=quiz, marks=int(marks[i])
                )

                db.session.add(quiz_question)
                total_marks += int(marks[i])
            quiz.marks = total_marks
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("Error Occured", "danger")
            return {"response": "Error Occured"}, 500
        flash("Quiz Added", "success")
        return {"response": "success"}, 200

    reqparse = reqparse.RequestParser()
    reqparse.add_argument("quiz_id", type=int, required=True, location="args")

    @ns.expect(reqparse, validate=True)
    @ns.marshal_with(QuizQuestionModel, mask=None)
    def get(self):
        if current_user.is_authenticated and current_user.role != "professor":
            return "Unauthorized access!", 401
        quizid = request.args.get("quiz_id")
        return Quiz.query.get_or_404(quizid)

    def put(self):
        if current_user.is_authenticated and current_user.role != "professor":
            return "Unauthorized access!", 401
        quiz = Quiz.query.get_or_404(request.form.get("id"))
        print(quiz)
        # question_ids_to_delete = [q.id for q in quiz.questions]
        if datetime.strptime(request.form.get("quiztime"), "%Y-%m-%dT%H:%M") - datetime.now() < timedelta(days=2):
            flash("Quiz time cannot be less than 2 days from now", "danger")
            return "Quiz time cannot be less than 2 days from now", 400
        quiztime=datetime.strptime(request.form.get("quiztime"), "%Y-%m-%dT%H:%M")
        quiz.date = quiztime
        # Clear the questions from the quiz
        quiz.questions.clear()

        # Delete the questions that are no longer associated with any quiz
        texts = request.form.getlist("text")
        questions_1 = request.form.getlist("option_1")
        questions_2 = request.form.getlist("option_2")
        questions_3 = request.form.getlist("option_3")
        questions_4 = request.form.getlist("option_4")
        marks = request.form.getlist("mark")
        question_count = len(texts)
        total_marks = 0
        for i in range(question_count):
            question = Question(
                text=texts[i],
                option_1=questions_1[i],
                option_2=questions_2[i],
                option_3=questions_3[i],
                option_4=questions_4[i],
                correct_option=request.form.get(f"correct_option_{i+1}"),
                author_id=current_user.id,
            )
            db.session.add(question)
            # quiz.questions.append(question)
            quiz_question = QuizQuestionAssosciation(
                question=question, quiz=quiz, marks=int(marks[i])
            )

            db.session.add(quiz_question)
            total_marks += int(marks[i])
        quiz.marks = total_marks
        try:
            db.session.commit()
            flash("Quiz Updated", "success")
            return {"response": "success"}, 200
        except:
            db.session.rollback()
            flash("Error Occured","danger")
            return {"response": "Error Occured"}, 500
    


@ns.route("/student_quizzes")
class stdquiz(Resource):
    @ns.marshal_list_with(quiz_model, mask=None)
    @login_required
    def get(self):
        quiz_list = []
        for course in current_user.courses:
            for quiz in course.quizzes:
                if quiz not in current_user.taken_quizzes:
                    if quiz.date - datetime.now() <= timedelta(
                        days=14
                    ) and quiz.date - datetime.now() >= timedelta(days=0, minutes=-30):
                        quiz_list.append(quiz)

        return quiz_list


student_marks_model = api.model(
    "StudentMarks",
    {
        "id": fields.Integer(readonly=True, description="User name"),
        "first_name": fields.String(),
        "last_name": fields.String(),
        "marks": fields.Integer(),
    },
)


@ns.route("/get_students/<int:quiz_id>")
class getstudents(Resource):
    @ns.marshal_list_with(student_marks_model, mask=None)
    def get(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        students_list = []
        for student in quiz.students:
            students_list.append(
                {
                    "id": student.id,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "marks": QuizStudentAssociation.query.filter_by(student_id=student.id,quiz_id=quiz.id).first().total_marks,
                }
            )
        return students_list
